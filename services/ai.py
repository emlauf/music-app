import requests
import os

import streamlit as st

def generate_tags(artist, track):

    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set")
        return ["chill", "vibes"]

    prompt = f"""
{artist} - {track} の音楽的特徴を
3〜5個の短いタグで出力してください。

例:
チル / エモい / 夜ドライブ
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        res = requests.post(url, json=body)

        # ★ ここ重要（デバッグ用）
        data = res.json()
        print("Gemini response:", data)

        res.raise_for_status()

        # ★ 安全に取り出す
        candidates = data.get("candidates")
        if not candidates:
            return ["vibes", "chill"]

        text = candidates[0]["content"]["parts"][0]["text"]

        # タグ整形
        tags = [t.strip("#・ \n") for t in text.split() if t]

        return tags[:5]

    except Exception as e:
        print("generate_tags error:", e)
        return ["vibes", "mood"]

def generate_diagnosis(tracks):
    return "あなたは“軽さと余裕を好むタイプ”です。"

def generate_reason(base_artist, base_track, target_artist, target_track):

    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    """
    2曲の類似理由を“エモく1文”で生成
    """

    prompt = f"""
あなたは音楽キュレーターです。

以下の2曲が「なぜ似ているか」を、日本語で1文で説明してください。

【元の曲】
{base_artist} - {base_track}

【似ている曲】
{target_artist} - {target_track}

ルール:
- 必ず1文（長すぎない）
- 音楽的観点（ノリ・雰囲気・ジャンル・感情）で説明
- 抽象すぎず、具体的すぎない
- 読んで「なるほど」と思える表現
- 同じ表現を使い回さない
- 20〜40文字くらいが理想

悪い例:
→ 雰囲気が似ている
→ 同じジャンル

良い例:
→ 軽快でキャッチーなラップと明るい空気感が共通している
→ チルなビートと内省的なムードが近い

出力は文章のみ（装飾不要）
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,  # バリエーション出す
            "topP": 0.9,
            "maxOutputTokens": 80
        }
    }

    try:
        res = requests.post(url, json=body)
        res.raise_for_status()

        text = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

        # 不要な改行・記号除去
        text = text.replace("\n", "").replace("→", "").strip()

        return text

    except Exception as e:
        print("generate_reason error:", e)
        return "心地よいノリと雰囲気が共通している"

@st.cache_data(ttl=86400, show_spinner=False)
def cached_generate_reason(base_artist, base_track, target_artist, target_track):
    return generate_reason(base_artist, base_track, target_artist, target_track)
