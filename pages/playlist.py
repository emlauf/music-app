import streamlit as st

def render():
    st.title("🎶 今日の音楽ルート")

    tracks = st.session_state.get("tracks", [])

    roles = ["始まり", "深める", "意外枠", "余韻"]

    for i, t in enumerate(tracks):
        role = roles[i % len(roles)]

        st.write(f"## {role}")
        st.write(f"{t['artist']} - {t['track']}")

        if t["spotify"]:
            st.markdown(f"[▶ 再生]({t['spotify']['url']})")

            st.components.v1.iframe(
                t["spotify"]["embed"],
                height=80
            )
        else:
            st.write("リンクなし")

    if st.button("診断へ", key="to_diag"):
        st.session_state.page = "diagnosis"
        st.rerun()