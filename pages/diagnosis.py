import streamlit as st
from services.ai import generate_diagnosis

def render():
    st.title("🧠 あなたの音楽タイプ")

    diagnosis = generate_diagnosis(st.session_state.tracks)

    st.write(diagnosis)

    if st.button("プロファイルを見る"):
        st.session_state.page = "profile"
        st.rerun()
