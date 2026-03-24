import requests
import os

def generate_tags(artist, track):
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"

    prompt = f"""
    {artist} - {track} の特徴を
    日本語の短いタグ3つで出力
    """

    body = {"contents":[{"parts":[{"text":prompt}]}]}

    res = requests.post(url, json=body)
    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]

    return text.split()

def generate_diagnosis(tracks):
    return "あなたは“軽さと余裕を好むタイプ”です。"
