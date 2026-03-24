import streamlit as st

# app.py で Secrets を取得
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
# Cloud ログに出力
if GEMINI_API_KEY is None:
    print("GEMINI_API_KEY not set")  # Cloud ログ
else:
    print("GEMINI_API_KEY length:", len(GEMINI_API_KEY))  # Cloud ログ

# ページ状態管理
if "page" not in st.session_state:
    st.session_state.page = "input"

# ルーティング
if st.session_state.page == "input":
    from pages import input
    input.render(api_key=GEMINI_API_KEY)

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
