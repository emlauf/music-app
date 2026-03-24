import streamlit as st

# app.py で Secrets を取得
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
print("GEMINI_API_KEY length:", len(GEMINI_API_KEY) if key else "None")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not set")

# ページ状態管理
if "page" not in st.session_state:
    st.session_state.page = "input"

# ルーティング
if st.session_state.page == "input":
    from pages import input
    input.render(GEMINI_API_KEY=GEMINI_API_KEY)

elif st.session_state.page == "loading":
    from pages import loading
    loading.render()

elif st.session_state.page == "result":
    from pages import result
    result.render()

elif st.session_state.page == "playlist":
    from pages import playlist
    playlist.render()

elif st.session_state.page == "diagnosis":
    from pages import diagnosis
    diagnosis.render()

elif st.session_state.page == "profile":
    from pages import profile
    profile.render()

elif st.session_state.page == "share":
    from pages import share
    share.render()
