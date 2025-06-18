import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_top_headlines(category="general"):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("Error: NEWS_API_KEY not found.")
        return []

    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=5&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print(f"Error from API: {data.get('message')}")
            return []

        articles = []
        for article in data.get("articles", []):
            if article.get("title"):
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "content": article.get("content", "")
                })
        return articles

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []