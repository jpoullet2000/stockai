import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Set up your API key (replace with your actual key or use environment variables for security)
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",  # Assuming this is the base URL for xAI's API
)

# Image generation prompt
prompt = "A serene landscape with a sunset over a calm lake."

# Make the API call
response = client.images.generate(
    prompt=prompt,
    model="grok-vision-beta", #"grok-2-vision-1212", # "grok-aurora",  # This is hypothetical; replace with the actual model name for image generation if different
    n=1,
    size="1024x1024",  # This might depend on what sizes Aurora supports
)

# The response will contain URL or base64 encoded data of the image
image_url = response.data[0].url
print(image_url)  # Or handle the image data as needed