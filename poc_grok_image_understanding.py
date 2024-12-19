import os
from openai import OpenAI
import os
import base64

from dotenv import load_dotenv

load_dotenv()


MODEL_NAME = "grok-vision-beta"
XAI_API_KEY = os.getenv("XAI_API_KEY")
image_path = "carte-continents-tropiques-oceans.png"

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# Getting the base64 string

base64_image = encode_image(image_path)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high",
                },
            },
            {
                "type": "text",
                "text": "What is on this image ?",
            },
        ],
    },
]

stream = client.chat.completions.create(
    model="grok-vision-beta",
    messages=messages,
    stream=True,
    temperature=0.01,
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="", flush=True)

