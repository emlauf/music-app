import streamlit as st
from utils.ai_parser import parse_music_input

def render():
    st.title("🎧 音楽ナビゲーター")

    text = st.text_input(
        "曲名・アーティスト・URLを入力",
        placeholder="jack harlow whats poppin"
    )

    if st.button("解析する"):
        if text:
            with st.spinner("AIで解析中..."):
                artist, track = parse_music_input(text)
                st.write("Debug:", artist, track)

            if artist and track:
                # ★ここが重要
                st.session_state.artist = artist
                st.session_state.track = track

                st.session_state.page = "loading"
                st.rerun()
            else:
                st.error("曲を特定できませんでした")