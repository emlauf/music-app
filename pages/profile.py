import streamlit as st

def render():
    st.title("📊 あなたの音楽プロファイル")

    st.write("よく出るタグ")
    st.write("#チル #夜っぽい #都会的")

    st.progress(0.8)

    if st.button("共有する"):
        st.session_state.page = "share"
        st.rerun()
