import streamlit as st
from utils.ai_parser import parse_music_input
import time

def render(api_key):
    st.title("🎧 音楽ナビゲーター")

    # 前回の結果をリセット
    st.session_state.artist = ""
    st.session_state.track = ""
    
    text = st.text_input(
        "曲名・アーティスト・URLを入力",
        placeholder="jack harlow whats poppin"
    )

    if st.button("解析する") and text:
        # ★少し待ってからリクエストすると安定
        time.sleep(0.2)

        artist, track, debug_text, debug_error = parse_music_input(text, api_key)

        # デバッグ情報をブラウザに表示
        if debug_text:
            st.text("AI raw response:")
            st.text(debug_text)
        if debug_error:
            st.text("AI parser error:")
            st.text(debug_error)

        if artist and track:
            st.session_state.artist = artist
            st.session_state.track = track
            st.session_state.page = "loading"
            st.rerun()
        else:
            st.error("曲を特定できませんでした")