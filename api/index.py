import os
import json
import logging
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from openai_chat import get_gpt_response
from faq import load_faq_data, match_faq

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise RuntimeError("Missing LINE credentials")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Load default reply
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)
default_reply = config.get("default_reply", "内容を理解できませんでした。")

# Load FAQ data
faq_entries = load_faq_data("faq.csv")

app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/api/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode("utf-8")
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    user_id = event.source.user_id
    message_text = event.message.text.strip()

    if message_text.lower() == "ping":
        reply_text = "pong"
    else:
        reply_text = match_faq(message_text, faq_entries)
        if not reply_text:
            try:
                reply_text = get_gpt_response(message_text)
            except Exception as e:
                logging.error(f"GPT error: {e}")
                reply_text = default_reply

    if event.reply_token != "dummy-reply-token":
        try:
            with ApiClient(configuration) as api_client:
                MessagingApi(api_client).reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=reply_text)]
                    )
                )
        except Exception as e:
            logging.error(f"LINE reply error: {e}")
    else:
        print(f"[TEST MODE] Reply skipped. Would send: {reply_text}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"[Unhandled Error] {exc}")
    return JSONResponse(status_code=500, content={"error": str(exc)})