import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Models that work with HF inference providers
CHAT_MODEL = "deepseek-ai/DeepSeek-V3-0324"
IMAGE_MODEL = "black-forest-labs/FLUX.1-dev"

BASE_URL = "https://router.huggingface.co/v1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def query_chat_model(prompt):
    API_URL = f"{BASE_URL}/chat/completions"

    payload = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 300
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"
    data = response.json()
    # Chat completion response format
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")

def generate_image(prompt):
    API_URL = f"{BASE_URL}/text-to-image"

    payload = {
        "model": IMAGE_MODEL,
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        return "generated_image.png"
    return f"Error {response.status_code}: {response.text}"