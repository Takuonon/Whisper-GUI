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
                },
                data={
                    "model": "whisper-1",  # モデルを指定
                    "response_format": "verbose_json",  # 詳細なJSONフォーマット
                    "timestamp_granularities[]": "word",  # 単語単位のタイムスタンプを指定
                },
            )

        if response.status_code == 200:
            # レスポンスのJSON全体を取得
            transcription = response.json()
            
            # 結果を画面に表示
            st.write("テキスト化結果（JSON形式）:")
            st.json(transcription)  # JSON全体を表示
            
            # JSONをダウンロード可能にする
            import json
            st.download_button(
                label="結果をJSON形式でダウンロード",
                data=json.dumps(transcription, ensure_ascii=False, indent=2),  # JSONを整形してダウンロード
                file_name="transcription.json",
                mime="application/json"
            )
        else:
            st.error(f"エラーが発生しました: {response.status_code}, {response.text}")

    except Exception as e:
        st.error(f"処理中にエラーが発生しました: {str(e)}")
    finally:
        # 一時ファイルの削除
        os.remove(temp_file_path)
