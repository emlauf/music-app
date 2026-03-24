import streamlit as st
from utils.ai_parser import parse_music_input

def render(GEMINI_API_KEY):
    st.title("🎧 音楽ナビゲーター")

    # 前回の結果をリセット
    st.session_state.artist = ""
    st.session_state.track = ""

    text = st.text_input(
        "曲名・アーティスト・URLを入力",
        placeholder="jack harlow whats poppin"
    )

    if st.button("解析する"):
        if text:
            with st.spinner("AIで解析中..."):
                artist, track, debug_text, debug_error = parse_music_input(text, GEMINI_API_KEY)
                st.write("Debug:", artist, track)

            # デバッグ情報をブラウザで確認
            if debug_text:
                st.text("AI raw response:")
                st.text(debug_text)
            if debug_error:
                st.text("AI parser error:")
                st.text(debug_error)

            if artist and track:
                # ★ここが重要
                st.session_state.artist = artist
                st.session_state.track = track

                st.session_state.page = "loading"
                st.rerun()
            else:
                st.error("曲を特定できませんでした")