# summarize.py (using gemini-1.5-flash-latest ✅)

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_article(article):
    title = article.get("title", "")
    content = article.get("content") or article.get("description") or ""

    prompt = f"Summarize this news article in 3 lines:\n\nTitle: {title}\n\nContent: {content}"

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini summarization failed: {e}"
