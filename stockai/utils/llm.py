import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


XAI_API_KEY = os.getenv("XAI_API_KEY")
llm_client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

