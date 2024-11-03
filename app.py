import streamlit as st
import requests
import os

# Streamlitアプリケーションの設定
st.title("Whisper API テキスト化ツール")
st.write("ファイルをアップロードし、APIキーを入力してテキストに変換します。")

# APIキーの入力とファイルアップロード
api_key = st.text_input("OpenAI API Key", type="password")
uploaded_file = st.file_uploader(
    "音声または動画ファイルをアップロード", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "mov", "mkv"]
)

# ボタンが押されたら処理を開始
if st.button("変換を開始") and api_key and uploaded_file:
    # ファイルをローカルに保存
    temp_file_path = f"./temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Whisper APIリクエスト
    try:
        with open(temp_file_path, "rb") as f:
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {api_key}"},
                files={
                    "file": (uploaded_file.name, f),
                    "model": (None, "whisper-1"),
                    "language": (None, "en"),  # 言語指定
                },
            )

        # 応答の処理
        if response.status_code == 200:
            transcription = response.json().get("text", "")
            st.write("テキスト化結果:")
            st.text_area("変換されたテキスト", transcription)
            st.download_button("結果をダウンロード", data=transcription, file_name="transcription.txt")
        else:
            st.error(f"エラーが発生しました: {response.status_code}")
    except Exception as e:
        st.error(f"処理中にエラーが発生しました: {str(e)}")
    finally:
        # 一時ファイルの削除
        os.remove(temp_file_path)
