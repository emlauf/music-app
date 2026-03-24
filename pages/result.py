import streamlit as st
from services.lastfm import get_similar_tracks
from services.spotify import search_track
from services.ai import generate_tags
from services.ai import generate_reason
from services.ai import cached_generate_reason

def render():
    st.title("🔍 分析結果")

    artist = st.session_state.get("artist")
    track = st.session_state.get("track")

    if not artist or not track:
        st.warning("先に曲を入力してください")
        st.stop()

    st.subheader(f"{artist} - {track}")

    # タグ
    tags = generate_tags(artist, track)
    st.write(" ".join([f"#{t.strip('#* ')}" for t in tags]))

    st.subheader("🎧 あなたに刺さる可能性が高い順")

    tracks = get_similar_tracks(artist, track)

    enriched_tracks = []

    for i, t in enumerate(tracks):
        st.write(f"### {t['artist']} - {t['track']}")
        reason = cached_generate_reason(
            artist,
            track,
            t["artist"],
            t["track"]
        )
        st.write(f"→ {reason}")

        spotify_data = search_track(t["artist"], t["track"])

        if spotify_data:
            st.markdown(f"[▶ 再生]({spotify_data['url']})")

            st.components.v1.iframe(
                spotify_data["embed"],
                height=80
            )
        else:
            st.write("⚠️ 再生リンクなし")

        enriched_tracks.append({
            "artist": t["artist"],
            "track": t["track"],
            "spotify": spotify_data
        })

    st.session_state.tracks = enriched_tracks

    if st.button("プレイリストへ", key="to_playlist"):
        st.session_state.page = "playlist"
        st.rerun()