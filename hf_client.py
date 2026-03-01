import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json",
}

def query_text_model(prompt: str) -> str:
    if not HF_API_KEY:
        return "Error: HF_API_KEY not set."

    url = "https://router.huggingface.co/v1/chat/completions"

    payload = {
        "model": TEXT_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert event planning assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=60)

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"

def generate_image(prompt: str) -> str:
    """
    Uses Pollinations AI (free, no key required)
    Returns a public image URL
    """
    encoded_prompt = urllib.parse.quote(
        f"Professional event poster, modern design, high quality, {prompt}"
    )

    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"