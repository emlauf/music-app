import os
import requests

def parse_music_input(user_input: str):

    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    """
    ユーザーの曖昧な入力を「アーティスト名」「曲名」に変換
    """

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
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        res = requests.post(url, json=body)
        res.raise_for_status()

        text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

        import json
        start = text.find("{")
        end = text.rfind("}") + 1
        parsed = json.loads(text[start:end])

        return parsed["artist"], parsed["track"]

    except Exception as e:
        print("AI parser error:", e)

        # ★ フォールバック（ここ超重要）
        return user_input, ""
