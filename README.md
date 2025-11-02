# LINE返信Bot - AI研修質問対応システム

AI研修の受講生からのLINE質問に対する回答案を自動生成し、Google Spreadsheetsに保存するツールです。

## 機能

- ✅ 質問文を入力すると、研修資料を基にAIが回答案を生成
- ✅ 質問と回答案をGoogle Spreadsheetsに自動保存
- ✅ Google AI Studio (Gemini) を使用した高品質な回答生成
- ✅ シンプルなコマンドライン操作

## 必要な準備

### 1. Google Cloud の設定

#### Google Sheets API の有効化（完了済み✓）
- Google Cloud Console でプロジェクト作成
- Google Sheets API を有効化
- サービスアカウント作成
- JSONキーをダウンロード

#### スプレッドシートの共有（完了済み✓）
- サービスアカウントのメールアドレスをスプレッドシートに共有
- 編集権限を付与

### 2. Google AI Studio の設定

#### APIキーの取得
1. https://aistudio.google.com/app/apikey にアクセス
2. 「Create API Key」をクリック
3. プロジェクトを選択（または新規作成）
4. APIキーをコピー

## セットアップ手順

### 1. 認証ファイルの配置

ダウンロードしたJSONファイル（サービスアカウントの認証情報）を `credentials.json` という名前で、このディレクトリに配置してください。

```bash
line_reply_bot/
├── credentials.json  ← ここに配置
├── line_reply_bot.py
└── ...
```

### 2. 環境変数の設定

`.env.template` をコピーして `.env` ファイルを作成し、必要な情報を入力してください。

```bash
# Windowsの場合
copy .env.template .env

# Mac/Linuxの場合
cp .env.template .env
```

`.env` ファイルを編集：

```env
# Google AI Studio (Gemini) API Key
GEMINI_API_KEY=あなたのGemini APIキー

# Google Spreadsheet ID（すでに設定済み）
SPREADSHEET_ID=1ZtwLI3QgrhLJjqjES0TI_RjSNW2Mqs7UN8weSslwtvw

# Google Service Account JSON file path
SERVICE_ACCOUNT_JSON=credentials.json
```

### 3. 研修資料の準備

`training_materials` フォルダに、AI研修の資料（テキストファイルまたはMarkdownファイル）を配置してください。

```bash
line_reply_bot/
└── training_materials/
    ├── 研修資料1.txt
    ├── 研修資料2.md
    └── FAQ.txt
```

対応形式：
- `.txt` ファイル
- `.md` ファイル

### 4. Pythonライブラリのインストール

必要なライブラリをインストールします。

#### 方法1: pip を使う場合

```bash
pip install -r requirements.txt
```

#### 方法2: pipがない場合

```bash
# pipのインストール（Ubuntu/Debian）
sudo apt update
sudo apt install python3-pip

# pipのインストール（Windows）
# Python公式サイトからインストーラーをダウンロードして再インストール
```

その後、再度 `pip install -r requirements.txt` を実行してください。

## 使い方

### 起動

```bash
python3 line_reply_bot.py
```

または

```bash
python line_reply_bot.py
```

### 操作手順

1. プログラムが起動すると、質問の入力待ち状態になります
2. LINEからの質問をコピー
3. ターミナルに貼り付けてEnterキーを押す
4. AIが回答案を生成します
5. 生成された回答が表示され、自動的にスプレッドシートに保存されます
6. 次の質問を入力できます

### 終了

`quit` または `exit` と入力してEnterキーを押すと終了します。

## スプレッドシートの確認

以下のURLでスプレッドシートを確認できます：

https://docs.google.com/spreadsheets/d/1ZtwLI3QgrhLJjqjES0TI_RjSNW2Mqs7UN8weSslwtvw/edit

保存される情報：
- 日時
- 質問原文
- 回答案
- ステータス（未送信/送信済み など）
- 備考

## プロジェクト構成

```
line_reply_bot/
├── README.md                 # このファイル
├── requirements.txt          # 必要なライブラリ一覧
├── .env.template             # 環境変数のテンプレート
├── .env                      # 環境変数（要作成）
├── .gitignore                # Git管理除外設定
├── credentials.json          # Google認証情報（要配置）
├── line_reply_bot.py         # メインスクリプト
└── training_materials/       # 研修資料フォルダ
    └── sample.txt            # サンプル資料
```

## トラブルシューティング

### エラー: GEMINI_API_KEYが設定されていません

→ `.env` ファイルに正しいAPIキーを設定してください

### エラー: 認証ファイルが見つかりません

→ `credentials.json` を正しい場所に配置してください

### エラー: スプレッドシートにアクセスできません

→ サービスアカウントのメールアドレスがスプレッドシートに共有されているか確認してください

### 研修資料が読み込まれない

→ `training_materials` フォルダに `.txt` または `.md` ファイルを配置してください

## 今後の拡張案

- [ ] LINE Messaging API との連携（自動取得・返信）
- [ ] 回答の承認フロー
- [ ] 複数のスプレッドシート対応
- [ ] 回答の品質評価機能
- [ ] よくある質問の自動学習

## ライセンス

このプロジェクトは内部利用を目的としています。

## サポート

質問や問題がある場合は、プロジェクト管理者に連絡してください。
