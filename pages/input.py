import streamlit as st

def render():
    st.title("🎧 音楽ナビゲーター")

    text = st.text_input(
        "曲名・アーティスト・URLを入力",
        placeholder="jack harlow whats poppin"
    )

    if st.button("解析する"):
        st.session_state.input_text = text
        st.session_state.page = "loading"
        st.rerun()
