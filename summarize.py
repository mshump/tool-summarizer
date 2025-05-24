import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import hashlib
import os
from notify import post_to_slack, summarize_with_huggingface #summarize_with_openai

TOOLS_FILE = "tools.json"
CACHE_FILE = "summarize_cache.json"
CUTOFF_DATE = datetime.now() - timedelta(days=90)

def hash_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all(["p", "li"])
        return " ".join(p.get_text() for p in paragraphs)
    except Exception as e:
        return ""

def run_summary():
    tools = json.load(open(TOOLS_FILE))
    cache = load_cache()
    for tool in tools:
        name = tool["name"]
        url = tool["url"]
        webhook = tool["webhook"]

        print(f"Fetching for {name} from {url}")
        text = fetch_content(url)
        if not text:
            post_to_slack(webhook, f"*{name}*: Could not fetch content.")
            continue

        content_hash = hash_text(text)
        if content_hash in cache:
            summary = cache[content_hash]["summary"]
        else:
            #summary = summarize_with_openai(text[:4000])  # truncate for token limit
            summary = summarize_with_huggingface(text[:1000])
            cache[content_hash] = {
                "summary": summary,
                "timestamp": str(datetime.now())
            }
            save_cache(cache)

        message = f"*{name} Summary:*\n{summary}\n<{url}|Read more>"
        post_to_slack(webhook, message)
