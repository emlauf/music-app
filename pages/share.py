import streamlit as st

def render():
    st.title("📤 結果を共有")

    st.button("画像保存")
    st.button("テキストコピー")
    st.button("Xに投稿")

    if st.button("もう一度"):
        st.session_state.page = "input"
        st.rerun()
