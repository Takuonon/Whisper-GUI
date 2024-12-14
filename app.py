import json
import requests
import streamlit as st
import pandas as pd

st.title("Whisper API テキスト化ツール")
st.write("ファイルをアップロードし、APIキーを入力してテキストに変換します。")
st.write("※webm形式のファイルを推奨します。mp4形式の場合、正常に動作しない可能性があります。")

api_key = st.text_input("APIキーを入力", type="password")
uploaded_file = st.file_uploader("音声ファイルをアップロード", type=["mp3", "wav", "webm", "mp4"])

# ラジオボタンで言語指定オプションを選択
language_option = st.radio(
    "言語指定 (任意):",
    ("オプションを指定しない", "日本語 (ja)", "英語 (en)")
)

# ボタンが押されたら処理を開始
if st.button("変換を開始") and api_key and uploaded_file:
    # ファイルをローカルに保存
    temp_file_path = f"./temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # リクエスト用データパラメータ
    data_params = {
        "model": "whisper-1",
        "response_format": "verbose_json",
        "timestamp_granularities[]": "word",
    }

    # 選択された言語オプションに応じてlanguageパラメータを追加
    if language_option == "日本語 (ja)":
        data_params["language"] = "ja"
    elif language_option == "英語 (en)":
        data_params["language"] = "en"
    # 「オプションを指定しない」場合は何も追加しない

    # Whisper APIリクエスト
    try:
        with open(temp_file_path, "rb") as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                files={
                    "file": (uploaded_file.name, f),
                },
                data=data_params,
            )

        if response.status_code == 200:
            # レスポンスのJSON全体を取得
            transcription = response.json()

            # テキスト化結果（JSON形式）を表示
            st.write("テキスト化結果（JSON形式）:")
            st.json(transcription)

            # JSONをダウンロード可能にする
            st.download_button(
                label="結果をJSON形式でダウンロード",
                data=json.dumps(transcription, ensure_ascii=False, indent=2),
                file_name="transcription.json",
                mime="application/json"
            )
        else:
            st.error(f"エラーが発生しました: {response.status_code}, {response.text}")

    except Exception as e:
        st.error(f"例外が発生しました: {e}")
