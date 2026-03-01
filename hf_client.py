import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

TEXT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
IMAGE_MODEL = "stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def query_text_model(prompt):
    API_URL = f"https://api-inference.huggingface.co/models/{TEXT_MODEL}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 500
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()[0]["generated_text"]


def generate_image(prompt):
    API_URL = f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}"
    
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        return "generated_image.png"
    
    return None