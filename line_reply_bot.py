#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE返信Bot - AI研修質問対応システム

このスクリプトは、ユーザーからのLINE質問に対する回答案を生成し、
Google Spreadsheetsに保存します。
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials

# .envファイルを読み込み
load_dotenv()


class LineReplyBot:
    """LINE返信Bot メインクラス"""

    def __init__(self):
        """初期化"""
        # 環境変数の読み込み
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.service_account_json = os.getenv('SERVICE_ACCOUNT_JSON', 'credentials.json')

        # 設定の検証
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEYが設定されていません。.envファイルを確認してください。")
        if not self.spreadsheet_id:
            raise ValueError("SPREADSHEET_IDが設定されていません。.envファイルを確認してください。")

        # Gemini APIの設定
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Google Sheets APIの設定
        self.setup_google_sheets()

        # 研修資料の読み込み
        self.training_materials = self.load_training_materials()

    def setup_google_sheets(self):
        """Google Sheets APIのセットアップ"""
        try:
            # 認証情報の読み込み
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            credentials = Credentials.from_service_account_file(
                self.service_account_json,
                scopes=scopes
            )

            # gspreadクライアントの初期化
            self.gc = gspread.authorize(credentials)

            # スプレッドシートを開く
            self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)

            # ワークシートの取得または作成
            try:
                self.worksheet = self.spreadsheet.worksheet('LINE返信ログ')
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title='LINE返信ログ',
                    rows=1000,
                    cols=5
                )
                # ヘッダー行を追加
                self.worksheet.append_row([
                    '日時', '質問原文', '回答案', 'ステータス', '備考'
                ])

            print("✓ Google Spreadsheetsに接続しました")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"認証ファイル '{self.service_account_json}' が見つかりません。"
            )
        except Exception as e:
            raise Exception(f"Google Sheets API の初期化に失敗しました: {str(e)}")

    def load_training_materials(self):
        """研修資料を読み込む"""
        materials_dir = Path(__file__).parent / 'training_materials'
        materials = []

        if not materials_dir.exists():
            print(f"⚠ 警告: 研修資料ディレクトリ '{materials_dir}' が見つかりません")
            return ""

        # .txtと.mdファイルを読み込み
        for file_path in materials_dir.glob('**/*.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # サロゲートペアなどの不正な文字を除去
                    content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                    materials.append(f"# {file_path.name}\n{content}\n")
                    print(f"✓ 読み込み: {file_path.name}")
            except Exception as e:
                print(f"⚠ エラー: {file_path.name} の読み込みに失敗 - {str(e)}")

        for file_path in materials_dir.glob('**/*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # サロゲートペアなどの不正な文字を除去
                    content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                    materials.append(f"# {file_path.name}\n{content}\n")
                    print(f"✓ 読み込み: {file_path.name}")
            except Exception as e:
                print(f"⚠ エラー: {file_path.name} の読み込みに失敗 - {str(e)}")

        if not materials:
            print("⚠ 警告: 研修資料が見つかりませんでした")
            return ""

        return "\n\n".join(materials)

    def generate_reply(self, question: str) -> str:
        """
        質問に対する回答を生成

        Args:
            question: ユーザーからの質問

        Returns:
            生成された回答
        """
        # プロンプトの構築
        prompt = f"""あなたはAI研修のサポート担当者です。
以下の研修資料を基に、受講生からの質問に丁寧に回答してください。

【研修資料】
{self.training_materials}

【質問】
{question}

【回答の条件】
1. LINE返信として適切な形式で回答してください
2. 簡潔で分かりやすい表現を心がけてください
3. 必要に応じて、研修資料の該当箇所を引用してください
4. 不明な点がある場合は、正直に「確認します」と伝えてください
5. 親しみやすく、丁寧な口調で回答してください

【回答】"""

        try:
            # Gemini APIで回答を生成
            print("回答を生成中...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = f"回答の生成に失敗しました: {str(e)}"
            print(f"✗ {error_msg}")
            return error_msg

    def save_to_spreadsheet(self, question: str, reply: str, status: str = "未送信", note: str = ""):
        """
        質問と回答をスプレッドシートに保存

        Args:
            question: 質問原文
            reply: 回答案
            status: ステータス（デフォルト: 未送信）
            note: 備考
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.worksheet.append_row([
                timestamp,
                question,
                reply,
                status,
                note
            ])
            print(f"✓ スプレッドシートに保存しました（{timestamp}）")
        except Exception as e:
            print(f"✗ スプレッドシートへの保存に失敗しました: {str(e)}")

    def run(self):
        """メインループ"""
        print("\n" + "="*60)
        print("LINE返信Bot - AI研修質問対応システム")
        print("="*60)

        if self.training_materials:
            print(f"\n✓ 研修資料を読み込みました")
        else:
            print(f"\n⚠ 研修資料が読み込まれていません")
            print(f"   'training_materials' フォルダに .txt または .md ファイルを配置してください")

        print("\n【使い方】")
        print("1. LINEからの質問をコピー")
        print("2. ここに貼り付けてEnter")
        print("3. 生成された回答がスプレッドシートに保存されます")
        print("4. 終了する場合は 'quit' または 'exit' と入力\n")

        while True:
            try:
                # 質問の入力を受け付け
                print("-" * 60)
                question = input("\n質問を入力してください: ").strip()

                # 終了コマンドのチェック
                if question.lower() in ['quit', 'exit', 'q', '終了']:
                    print("\nプログラムを終了します。")
                    break

                # 空入力のチェック
                if not question:
                    print("質問が入力されていません。もう一度入力してください。")
                    continue

                # 回答を生成
                reply = self.generate_reply(question)

                # 結果を表示
                print("\n" + "="*60)
                print("【生成された回答】")
                print("="*60)
                print(reply)
                print("="*60)

                # スプレッドシートに保存
                self.save_to_spreadsheet(question, reply)

                print("\n✓ 処理が完了しました")

            except KeyboardInterrupt:
                print("\n\nプログラムを終了します。")
                break
            except Exception as e:
                print(f"\n✗ エラーが発生しました: {str(e)}")
                continue


def main():
    """メイン関数"""
    try:
        bot = LineReplyBot()
        bot.run()
    except Exception as e:
        print(f"\n✗ 初期化エラー: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
