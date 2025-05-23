import os
import requests
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def post_to_slack(webhook, message):
    response = requests.post(webhook, json={"text": message})
    return response.status_code == 200

def summarize_with_openai(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this changelog or blog update in 2-4 sentences, focusing on user-relevant updates."},
            {"role": "user", "content": text}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()
