# LINE Bot プロジェクト（FastAPI + LINE SDK v3）

この LINE Bot は、ユーザーのメッセージに応じて以下の機能を提供します：

- Ping 応答（“ping” → “pong”）
- 物件に関する問い合わせフロー（物件→エリア→予算）
- 目的リンク案内（CSVベースのキーワードマッチ）
- FAQ 自動応答（CSVベース）
- OpenAI GPT による汎用チャット応答
- Google Sheets への会話ログ出力
- 会話ログの S3 暗号化保存（AES-GCM）
- 個人情報マスク（氏名・電話番号などを伏字に置換）

FastAPI による Webhook サーバーとして構成されており、Vercel へのデプロイに対応しています。

## 使用技術

- Python 3.13
- FastAPI
- LINE Messaging API SDK v3
- gspread / Google Sheets API
- OpenAI API
- boto3（AWS S3 SDK）
- cryptography（AES暗号化）
- python-dotenv
- mangum（Vercel対応）


## 機能仕様

### 1. Ping–Pong 機能

- ユーザーが「ping」と送信すると、Bot は「pong」と返信します。

### 2. Webhook 処理

- POSTエンドポイント： `/api/callback`
- X-Line-Signature 検証付き
- 処理の優先順：
  1. 目的リンク返信（CSVによるキーワードマッチ）
  2. FAQ応答（CSVによる質問マッチ）
  3. 物件問い合わせフロー（エリア → 予算）
  4. OpenAI GPTによる応答

### 3. Google Sheets ログ出力

- `.env` の `GOOGLE_SHEET_ID` と `GOOGLE_SERVICE_ACCOUNT_JSON` によりスプレッドシートに記録
- 記録内容：タイムスタンプ・ユーザーID・ユーザー発言・Bot応答

### 4. S3 暗号化ログ保存

- `.env` に AWS 認証情報と S3 設定を記述
- `s3_logger.py` でログを AES-GCM により暗号化し `.enc` ファイルとして S3 に保存

### 5. 個人情報マスキング

- 入力/出力両方に対して個人情報（氏名・電話番号など）を自動で伏字化
- `mask.py` で正規表現ベースの検出と置換を実施

### 6. 環境切り替え対応

- `.env` の `ENV=staging` または `ENV=production` によって動作切り替え（ロギングのON/OFFなど）

### 7. エラー処理

- 全体に FastAPI の `exception_handler` を実装
- ステータスコード 500 で JSON `{ "error": "..." }` を返却

## ローカル開発手順

### 1. pipenv で依存パッケージをインストール

```bash
pipenv install --dev
pipenv shell

```

## 環境変数（.env）

このBotを動かすには、以下の環境変数を設定してください。

| 変数名 | 説明 |
|--------|------|
| `LINE_CHANNEL_SECRET` | LINE公式アカウントのチャネルシークレット |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE公式アカウントのチャネルアクセストークン |
| `OPENAI_API_KEY` | OpenAI APIキー（GPT応答に使用） |
| `GOOGLE_SHEET_ID` | 会話ログを書き込むGoogleスプレッドシートのID |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | GoogleサービスアカウントのJSON（1行の文字列形式） |
| `FAQ_PATH` | FAQ CSVファイルのパス（例：`faq.csv`） |
| `GOALS_PATH` | リンク誘導CSVファイルのパス（例：`goals.csv`） |
| `ENV` | 実行環境を指定（`production` または `staging`） |
| `AWS_ACCESS_KEY_ID` | AWS S3へアクセスするためのアクセスキー |
| `AWS_SECRET_ACCESS_KEY` | AWS S3へアクセスするためのシークレットキー |
| `AWS_REGION` | S3バケットのリージョン（例：`ap-northeast-1`） |
| `S3_BUCKET_NAME` | 会話ログをアップロードするS3バケット名 |
| `S3_LOG_PREFIX` | S3バケット内の保存先プレフィックス（例：`logs/`） |

`.env.example` ファイルを参考に `.env` を作成し、ローカルまたは Vercel の環境変数に反映してください。


.env.example を参考に `.env` を作成してください。