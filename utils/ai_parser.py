import os
import requests
import re
import json
import streamlit as st
import time

# utils/ai_parser.py
import requests
import re
import json
import time
import streamlit as st

def parse_music_input(user_input: str, GEMINI_API_KEY: str, retries: int = 3, base_wait: float = 0.5):
    """
    ユーザーの曖昧な入力を「アーティスト名」「曲名」に変換
    Cloud安定版（指数バックオフ + キャッシュ対応）
    """

    # キャッシュチェック
    cache = st.session_state.get("music_cache", {})
    if user_input in cache:
        artist, track = cache[user_input]
        return artist, track, "Cached response", None

    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY が設定されていません")
        print("GEMINI_API_KEY not set")
        return user_input, "", None, "Missing GEMINI_API_KEY"

    prompt = f"""
以下の音楽検索入力を解析してください。

入力: "{user_input}"

やること:
- アーティスト名と曲名を抽出
- スペルミスを修正
- 正しい英語表記にする
- 必ずJSON形式で返す

出力形式:
{{
  "artist": "...",
  "track": "..."
}}

例:
入力: jack harlo whats poppin
出力:
{{
  "artist": "Jack Harlow",
  "track": "WHATS POPPIN"
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}

    wait = base_wait
    for attempt in range(1, retries + 1):
        try:
            res = requests.post(url, json=body)
            
            if res.status_code == 429:
                print(f"Rate limited (429), retry {attempt}/{retries}, waiting {wait} sec")
                time.sleep(wait)
                wait *= 2  # 指数バックオフ
                continue

            res.raise_for_status()

            text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

            # Cloudログとブラウザで確認
            print("AI raw response:", text)
            st.text("AI raw response:")
            st.text(text)

            # JSON部分だけ抽出
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                parsed = json.loads(match.group())
                artist = parsed.get("artist", "").strip()
                track = parsed.get("track", "").strip()

                # キャッシュ保存
                if "music_cache" not in st.session_state:
                    st.session_state.music_cache = {}
                st.session_state.music_cache[user_input] = (artist, track)

                return artist, track, text, None
            else:
                return user_input, "", text, "No JSON found in response"

        except requests.exceptions.HTTPError as e:
            print("HTTPError:", e, res.text)
            st.text("AI parser HTTPError:")
            st.text(res.text)
            return user_input, "", None, str(e)
        except Exception as e:
            print("AI parser error:", e)
            st.text("AI parser error:")
            st.text(str(e))
            return user_input, "", None, str(e)

    return user_input, "", None, "Failed after retries due to 429"