import requests
import os
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


# =========================
# アクセストークン取得（キャッシュ）
# =========================
@st.cache_data(ttl=3500)  # 約1時間キャッシュ
def get_access_token():
    url = "https://accounts.spotify.com/api/token"

    data = {
        "grant_type": "client_credentials"
    }

    try:
        res = requests.post(
            url,
            data=data,
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=10
        )
        res.raise_for_status()

        token = res.json().get("access_token")

        if not token:
            raise ValueError("アクセストークン取得失敗")

        return token

    except Exception as e:
        print("Spotify token error:", e)
        return None


# =========================
# 曲検索（キャッシュ）
# =========================
@st.cache_data(ttl=86400)  # 24時間キャッシュ
def search_track(artist, track):
    token = get_access_token()

    if not token:
        return None

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query = f"{track} {artist}"

    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    try:
        res = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        res.raise_for_status()

        data = res.json()
        items = data.get("tracks", {}).get("items", [])

        if not items:
            return None

        track_id = items[0]["id"]

        return {
            "url": f"https://open.spotify.com/track/{track_id}",
            "embed": f"https://open.spotify.com/embed/track/{track_id}"
        }

    except Exception as e:
        print("Spotify search error:", e)
        return None