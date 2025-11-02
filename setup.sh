#!/bin/bash
# LINE返信Bot セットアップスクリプト

echo "=========================================="
echo "LINE返信Bot セットアップ"
echo "=========================================="
echo ""

# 1. Python確認
echo "1. Pythonのバージョン確認..."
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python3がインストールされていません"
    exit 1
fi
python3 --version
echo ""

# 2. 仮想環境の作成
echo "2. Python仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 仮想環境を作成しました"
else
    echo "✓ 仮想環境は既に存在します"
fi
echo ""

# 3. ライブラリのインストール
echo "3. 必要なライブラリをインストール中..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
echo "✓ ライブラリのインストールが完了しました"
echo ""

# 4. .envファイルの確認
echo "4. 設定ファイルの確認..."
if [ ! -f ".env" ]; then
    echo "⚠ .envファイルが見つかりません"
    echo "  .env.templateをコピーして.envを作成してください："
    echo "  cp .env.template .env"
    echo ""
else
    echo "✓ .envファイルが存在します"
fi

# 5. credentials.jsonの確認
if [ ! -f "credentials.json" ]; then
    echo "⚠ credentials.jsonが見つかりません"
    echo "  Google Cloud ConsoleからダウンロードしたJSONファイルを"
    echo "  このフォルダに credentials.json として配置してください"
    echo ""
else
    echo "✓ credentials.jsonが存在します"
fi

# 6. 研修資料の確認
if [ ! -d "training_materials" ]; then
    mkdir -p training_materials
    echo "✓ training_materialsフォルダを作成しました"
else
    echo "✓ training_materialsフォルダが存在します"
fi

file_count=$(find training_materials -type f \( -name "*.txt" -o -name "*.md" \) | wc -l)
if [ $file_count -eq 0 ] || [ $file_count -eq 1 ]; then
    echo "⚠ 研修資料が見つかりません"
    echo "  training_materialsフォルダに .txt または .md ファイルを配置してください"
    echo ""
else
    echo "✓ 研修資料ファイル: $file_count 個"
fi

echo ""
echo "=========================================="
echo "セットアップ完了！"
echo "=========================================="
echo ""
echo "次のステップ："
echo "1. .envファイルを編集してAPIキーを設定"
echo "2. credentials.jsonを配置"
echo "3. training_materialsフォルダに研修資料を配置"
echo "4. 実行: ./venv/bin/python3 line_reply_bot.py"
echo ""
