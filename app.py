#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE返信Bot - Streamlit Webアプリ版

このアプリは、AI研修の質問に対する回答案を自動生成し、
Google Spreadsheetsに保存します。
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
import json


# ページ設定
st.set_page_config(
    page_title="LINE返信Bot",
    page_icon="💬",
    layout="wide"
)


@st.cache_resource
def initialize_gemini():
    """Gemini APIの初期化"""
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')


@st.cache_resource
def initialize_sheets():
    """Google Sheets APIの初期化"""
    # secrets.tomlから認証情報を取得
    service_account_info = dict(st.secrets["gcp_service_account"])

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=scopes
    )

    gc = gspread.authorize(credentials)
    spreadsheet_id = st.secrets["SPREADSHEET_ID"]
    spreadsheet = gc.open_by_key(spreadsheet_id)

    # ワークシートの取得または作成
    try:
        worksheet = spreadsheet.worksheet('LINE返信ログ')
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title='LINE返信ログ',
            rows=1000,
            cols=5
        )
        # ヘッダー行を追加
        worksheet.append_row([
            '日時', '質問原文', '回答案', 'ステータス', '備考'
        ])

    return worksheet


@st.cache_data
def load_training_materials():
    """研修資料を読み込む"""
    materials_dir = Path(__file__).parent / 'training_materials'
    materials = []

    if not materials_dir.exists():
        return ""

    # .txtと.mdファイルを読み込み
    for file_path in materials_dir.glob('**/*.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # サロゲートペアなどの不正な文字を除去
                content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                materials.append(f"# {file_path.name}\n{content}\n")
        except Exception as e:
            st.warning(f"⚠ エラー: {file_path.name} の読み込みに失敗 - {str(e)}")

    for file_path in materials_dir.glob('**/*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # サロゲートペアなどの不正な文字を除去
                content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
                materials.append(f"# {file_path.name}\n{content}\n")
        except Exception as e:
            st.warning(f"⚠ エラー: {file_path.name} の読み込みに失敗 - {str(e)}")

    return "\n\n".join(materials)


def generate_reply(model, question: str, training_materials: str) -> str:
    """質問に対する回答を生成"""
    prompt = f"""あなたはAI研修のサポート担当者です。
受講生からの質問に対して、研修資料の内容を基に具体的で実用的な回答をしてください。

【研修資料】
{training_materials}

【質問】
{question}

【回答の条件】
1. 質問内容に直接答えてください
2. 研修資料の具体的な内容を使って説明してください
3. ファイル名やフォルダ構造については言及しないでください
4. 簡潔で分かりやすく、実務で役立つ回答を心がけてください
5. 不明な点がある場合は、正直に「確認します」と伝えてください

【回答】"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"回答の生成に失敗しました: {str(e)}"


def save_to_spreadsheet(worksheet, question: str, reply: str, status: str = "未送信", note: str = ""):
    """質問と回答をスプレッドシートに保存"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        worksheet.append_row([
            timestamp,
            question,
            reply,
            status,
            note
        ])
        return True
    except Exception as e:
        st.error(f"スプレッドシートへの保存に失敗しました: {str(e)}")
        return False


# メインアプリ
def main():
    st.title("💬 LINE返信Bot")
    st.markdown("AI研修の質問に対する回答案を自動生成します")

    # サイドバー
    with st.sidebar:
        st.header("📊 情報")

        # 研修資料の読み込み状況
        training_materials = load_training_materials()
        if training_materials:
            st.success("✓ 研修資料を読み込みました")
        else:
            st.warning("⚠ 研修資料が読み込まれていません")

        st.markdown("---")
        st.markdown("### 使い方")
        st.markdown("""
        1. 質問を入力
        2. 「回答を生成」ボタンをクリック
        3. 生成された回答を確認
        4. 自動的にスプレッドシートに保存されます
        """)

        st.markdown("---")
        st.markdown("### スプレッドシート")
        spreadsheet_id = st.secrets["SPREADSHEET_ID"]
        st.markdown(f"[📊 スプレッドシートを開く](https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit)")

    # メインエリア
    st.markdown("---")

    # 質問入力
    question = st.text_area(
        "質問を入力してください",
        height=150,
        placeholder="例：AI研修の概要について教えてください"
    )

    # 回答生成ボタン
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("🤖 回答を生成", type="primary", use_container_width=True)

    # 回答生成処理
    if generate_button:
        if not question.strip():
            st.warning("⚠ 質問を入力してください")
        else:
            with st.spinner("回答を生成中..."):
                try:
                    # Gemini APIで回答生成
                    model = initialize_gemini()
                    reply = generate_reply(model, question, training_materials)

                    # 結果表示
                    st.markdown("---")
                    st.subheader("📝 生成された回答")
                    st.markdown(f"**質問:** {question}")
                    st.markdown("**回答:**")
                    st.info(reply)

                    # スプレッドシートに保存
                    with st.spinner("スプレッドシートに保存中..."):
                        worksheet = initialize_sheets()
                        if save_to_spreadsheet(worksheet, question, reply):
                            st.success("✓ スプレッドシートに保存しました")

                    # コピーボタン
                    st.markdown("---")
                    st.code(reply, language=None)

                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

    # フッター
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>LINE返信Bot - AI研修質問対応システム</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
