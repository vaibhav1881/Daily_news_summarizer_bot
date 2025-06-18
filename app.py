import streamlit as st
from utils.fetch_news import fetch_top_headlines
from utils.summarize import summarize_article
import json

st.set_page_config(page_title="Daily News Summarizer", layout="wide")
st.title("📰 Daily News Summarizer Bot")
st.markdown("Get quick 2-line summaries of today's top headlines!")

category = st.selectbox("Select News Category", [
    "general", "technology", "business", "entertainment", "health", "science", "sports"
])

if st.button("Summarize News"):
    with st.spinner("Fetching and summarizing news..."):
        articles = fetch_top_headlines(category)
        if not articles:
            st.error("Could not fetch news. Please check your API key or network connection.")
        else:
            for idx, article in enumerate(articles):
                if isinstance(article, str):
                    try:
                        article = json.loads(article)
                    except json.JSONDecodeError:
                        st.error(f"Error decoding article {idx + 1}")
                        continue
                try:
                    summary = summarize_article(article)
                    st.subheader(f"🟢 News {idx + 1}")
                    st.markdown(f"**Summary:** {summary}")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Error summarizing article {idx + 1}: {e}")