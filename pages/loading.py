import streamlit as st
import time

def render():
    st.write("🎵 音楽を解析中...")

    st.write("・似てる曲を探しています")
    st.write("・雰囲気タグを生成しています")
    st.write("・プレイリストを構築しています")

    time.sleep(2)

    st.session_state.page = "result"
    st.rerun()
