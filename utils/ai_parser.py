import os
import requests
import re
import json
import streamlit as st

def parse_music_input(user_input: str, GEMINI_API_KEY: str):
    """
    ユーザーの曖昧な入力を「アーティスト名」「曲名」に変換
    安定動作版
    """

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

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        res = requests.post(url, json=body)
        res.raise_for_status()

        text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

        # ★ブラウザとCloudログで確認
        print("AI raw response:", text)
        st.text("AI raw response:")
        st.text(text)

        # JSON部分だけ抽出
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            artist = parsed.get("artist", "").strip()
            track = parsed.get("track", "").strip()
            return artist, track, text, None
        else:
            return user_input, "", text, "No JSON found in response"

    except Exception as e:
        print("AI parser error:", e)
        st.text("AI parser error:")
        st.text(str(e))
        return user_input, "", None, str(e)
