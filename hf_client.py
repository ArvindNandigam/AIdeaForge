import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

CHAT_MODEL = "HuggingFaceH4/zephyr-7b-beta"

BASE_URL = "https://router.huggingface.co/v1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def query_text_model(prompt):
    API_URL = f"{BASE_URL}/chat/completions"

    payload = {
        "model": CHAT_MODEL,
        "provider": "hf-inference",
        "messages": [
            {"role": "system", "content": "You are a helpful campus innovation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()
    return data["choices"][0]["message"]["content"]