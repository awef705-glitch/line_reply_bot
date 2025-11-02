# LINE返信Bot - Streamlit Cloud デプロイ手順

このドキュメントでは、LINE返信BotをStreamlit Cloudにデプロイする手順を説明します。

## 目次
1. [概要](#概要)
2. [事前準備](#事前準備)
3. [GitHubへのプッシュ](#githubへのプッシュ)
4. [Streamlit Cloudのセットアップ](#streamlit-cloudのセットアップ)
5. [Secretsの設定](#secretsの設定)
6. [デプロイの確認](#デプロイの確認)
7. [URLの共有](#urlの共有)
8. [トラブルシューティング](#トラブルシューティング)

## 概要

Streamlit Cloudは無料でWebアプリをホスティングできるサービスです。以下の利点があります：

- 完全無料（パブリックリポジトリの場合）
- 自分のPCを起動し続ける必要なし
- URLを共有するだけで他の人が使える
- 自動デプロイ（GitHubにプッシュすると自動更新）

## 事前準備

以下が必要です：

### 1. GitHubアカウント
- まだない場合は https://github.com で作成

### 2. 必要な情報を準備
- ✅ Gemini API Key（既に取得済み）
- ✅ Google Spreadsheet ID（既に取得済み）
- ✅ credentials.json の内容（サービスアカウントのJSON）

### 3. 必要なファイル
以下のファイルが揃っていることを確認：
```
line_reply_bot/
├── app.py                              # Streamlitアプリ本体
├── requirements.txt                    # 依存ライブラリ
├── .streamlit/
│   └── secrets.toml.template          # Secrets設定のテンプレート
└── training_materials/                 # 研修資料フォルダ
    └── *.txt または *.md ファイル
```

## GitHubへのプッシュ

### ステップ1: リポジトリの確認

現在のリポジトリ状態を確認：
```bash
cd /mnt/c/Users/awef7/Documents/00_GitHub/01_Taniuchi/研修資料/line_reply_bot
git status
```

### ステップ2: ファイルをコミット

```bash
# 新しいファイルを追加
git add app.py requirements.txt .streamlit/ DEPLOY.md

# 研修資料も追加（機密情報がないことを確認）
git add training_materials/

# コミット
git commit -m "Add Streamlit web app for LINE reply bot"
```

### ステップ3: GitHubにプッシュ

```bash
# まだリモートリポジトリがない場合
# GitHubで新しいリポジトリを作成してから：
git remote add origin https://github.com/YOUR_USERNAME/line_reply_bot.git
git branch -M main
git push -u origin main

# 既にリモートリポジトリがある場合
git push
```

⚠️ **重要**: `.gitignore`に以下が含まれていることを確認してください：
```
.env
credentials.json
.streamlit/secrets.toml
venv/
```

## Streamlit Cloudのセットアップ

### ステップ1: Streamlit Cloudにアクセス

1. https://share.streamlit.io にアクセス
2. 「Sign up with GitHub」をクリック
3. GitHubアカウントでログイン
4. Streamlit CloudにGitHubアクセスを許可

### ステップ2: 新しいアプリをデプロイ

1. 「New app」ボタンをクリック
2. 以下を設定：
   - **Repository**: `YOUR_USERNAME/line_reply_bot`（または該当リポジトリ）
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: 好きなURL名を設定（例: `your-name-line-reply-bot`）

3. 「Advanced settings」をクリック（重要！）

## Secretsの設定

デプロイ前に、機密情報を設定する必要があります。

### ステップ1: Secrets設定画面を開く

「Advanced settings」内の「Secrets」セクションに以下を貼り付け：

### ステップ2: Secretsの内容を記入

`.streamlit/secrets.toml.template`の内容をコピーして、実際の値に置き換えます：

```toml
# Gemini API Key
GEMINI_API_KEY = "あなたの実際のGemini APIキー"

# Google Spreadsheet ID
SPREADSHEET_ID = "1ZtwLI3QgrhLJjqjES0TI_RjSNW2Mqs7UN8weSslwtvw"

# Google Cloud Service Account の認証情報
# credentials.json の中身をそのまま以下の形式で貼り付け
[gcp_service_account]
type = "service_account"
project_id = "実際のプロジェクトID"
private_key_id = "実際のprivate_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\n実際の秘密鍵\n-----END PRIVATE KEY-----\n"
client_email = "実際のサービスアカウントメール@プロジェクト.iam.gserviceaccount.com"
client_id = "実際のclient_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/実際のアカウント名%40プロジェクト.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

### ステップ3: credentials.jsonの値を取得する方法

`credentials.json`ファイルを開いて、各フィールドの値をコピーします：

```bash
# ファイルの内容を表示
cat credentials.json
```

JSONの各キー（type, project_id, private_key, client_email等）を、上記のTOML形式に転記します。

⚠️ **注意点**:
- `private_key`は改行コード（\n）を含めて正確にコピー
- ダブルクォートは削除しないこと
- TOMLでは`=`の周りにスペースが必要

### ステップ4: デプロイを実行

1. Secrets設定が完了したら「Deploy!」ボタンをクリック
2. デプロイには2-5分程度かかります
3. ログを確認しながら待機

## デプロイの確認

### 成功した場合

- アプリのURLが表示されます（例: `https://your-name-line-reply-bot.streamlit.app`）
- ブラウザで開くと、LINE返信Botの画面が表示されます

### 確認項目

1. ✅ サイドバーに「✓ 研修資料を読み込みました」と表示される
2. ✅ 質問を入力して「🤖 回答を生成」ボタンが動作する
3. ✅ 生成された回答が表示される
4. ✅ スプレッドシートにデータが保存される

### エラーが出た場合

デプロイログを確認して、以下をチェック：

1. **ModuleNotFoundError**: `requirements.txt`に必要なライブラリが記載されているか確認
2. **Secrets関連エラー**: Secrets設定が正確か確認（特にJSONの形式）
3. **Google Sheets API エラー**: サービスアカウントにスプレッドシートの共有権限があるか確認

## URLの共有

### ステップ1: アプリのURLを取得

デプロイ完了後、以下のようなURLが発行されます：
```
https://your-name-line-reply-bot.streamlit.app
```

### ステップ2: 他の人に共有

このURLを共有するだけで、誰でもアプリにアクセスできます：

- メール、チャット、Slackなどで共有
- ブックマークして社内で使用
- 特別な設定は不要

### ステップ3: アクセス制限（オプション）

パブリックアプリは誰でもアクセス可能です。制限したい場合は：

1. Streamlit Cloudの設定で「Private app」に変更
   - ※ Proプラン（有料）が必要
2. または、アプリ内でパスワード認証を実装

## トラブルシューティング

### 問題1: アプリが起動しない

**症状**: デプロイ後に白い画面やエラーページ

**解決策**:
1. Streamlit Cloud のログを確認
2. `app.py`のパスが正しいか確認
3. `requirements.txt`が正しくコミットされているか確認

### 問題2: Secrets読み込みエラー

**症状**: `KeyError: 'GEMINI_API_KEY'` などのエラー

**解決策**:
1. Streamlit Cloud の Settings → Secrets を開く
2. TOML形式が正確か確認（特にインデント）
3. キー名のスペルミスがないか確認
4. 「Save」ボタンを押し忘れていないか確認

### 問題3: Google Sheets接続エラー

**症状**: `Insufficient Permission` などのエラー

**解決策**:
1. スプレッドシートの共有設定を確認
2. サービスアカウントのメールアドレス（client_email）に編集権限があるか確認
3. Google Cloud Console でSheets APIが有効か確認

### 問題4: 研修資料が読み込まれない

**症状**: サイドバーに「⚠ 研修資料が読み込まれていません」

**解決策**:
1. `training_materials/`フォルダがGitHubにプッシュされているか確認
2. フォルダ内に`.txt`または`.md`ファイルがあるか確認
3. GitHubリポジトリで実際にファイルが見えるか確認

### 問題5: アプリの更新が反映されない

**症状**: コードを変更してプッシュしたのに、アプリが古いまま

**解決策**:
1. GitHubにプッシュが完了しているか確認：`git push`
2. Streamlit Cloud は自動デプロイに30秒〜数分かかる場合がある
3. Streamlit Cloud の管理画面で「Reboot app」をクリック
4. ブラウザのキャッシュをクリア（Ctrl+Shift+R / Cmd+Shift+R）

## アプリの管理

### ログの確認

Streamlit Cloud の管理画面から：
1. 「Manage app」をクリック
2. 「Logs」タブでリアルタイムログを確認

### アプリの再起動

エラーが発生した場合：
1. 「Manage app」→「Reboot app」
2. アプリが再起動され、最新のコードが適用される

### アプリの削除

不要になった場合：
1. 「Manage app」→「Settings」
2. 「Delete app」で削除

## 次のステップ

デプロイが完了したら：

1. ✅ URLを関係者に共有
2. ✅ 実際に質問を入力して動作確認
3. ✅ スプレッドシートにデータが蓄積されることを確認
4. ✅ 必要に応じて研修資料を追加・更新

### 研修資料の更新方法

1. ローカルの`training_materials/`フォルダに新しいファイルを追加
2. Gitでコミット＆プッシュ：
   ```bash
   git add training_materials/
   git commit -m "Add new training materials"
   git push
   ```
3. Streamlit Cloud が自動的に再デプロイ（2-3分）
4. アプリが更新され、新しい研修資料が反映される

## サポート

問題が解決しない場合：

- Streamlit公式ドキュメント: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- このREADME.mdファイルも参照

---

**作成日**: 2025-11-03
**最終更新**: 2025-11-03
