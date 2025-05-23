import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def post_to_slack(webhook, message):
    response = requests.post(webhook, json={"text": message})
    return response.status_code == 200

def summarize_with_openai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize this changelog or blog update in 2-4 sentences, focusing on user-relevant updates."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI summarization failed: {e}")
        return "⚠️ Summarization failed."