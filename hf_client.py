import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

# Try a model supported by inference providers
TEXT_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"

BASE_URL = "https://router.huggingface.co/v1"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def query_text_model(prompt: str) -> str:
    url = f"{BASE_URL}/chat/completions"

    payload = {
        "model": TEXT_MODEL,
        "provider": "auto",  # Let HF choose a provider if available
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for campus event planning."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 450
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    data = response.json()
    # Chat completion returns nested structure
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")

def generate_image(prompt: str):
    image_model = "runwayml/stable-diffusion-v1-5"
    API_URL = f"https://api-inference.huggingface.co/models/{image_model}"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    print("IMAGE STATUS:", response.status_code)
    print("IMAGE RESPONSE:", response.text)

    if response.status_code == 200:
        return response.content
    else:
        return None