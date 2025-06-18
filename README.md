# 📰 Daily News Summarizer Bot

An AI-powered web app that fetches the latest news, summarizes articles using Google Gemini, translates summaries to Hindi or Marathi, and provides text-to-speech playback.  
Built with **Streamlit** for an interactive UI.

---

## 🚀 Features

- **Fetch Top News:** Get the latest headlines by category or custom topic.
- **AI Summarization:** Summarizes news articles in 3 lines using Gemini API.
- **Voice Input:** Search news by speaking your query (speech-to-text).
- **Translation:** Translate summaries to Hindi or Marathi.
- **Text-to-Speech:** Listen to summaries in your chosen language.
- **Ask Questions:** Chatbot answers your questions about the fetched news.

---

## 🛠️ Setup

### 1. Clone the Repository

```sh
git clone https://github.com/vaibhav1881/Daily_news_summarizer_bot.git
cd Daily_news_summarizer_bot
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory with your API keys:

```
NEWS_API_KEY=your_newsapi_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## 💻 Usage

### Run the Streamlit App

```sh
streamlit run app.py
```

The app will open in your browser.

---

## 🧩 Project Structure

```
.
├── app.py
├── utils/
│   ├── fetch_news.py
│   └── summarize.py
├── requirements.txt
└── .env
```

---

## ✨ Credits

- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev/)
- [NewsAPI](https://newsapi.org/)
- [gTTS](https://pypi.org/project/gTTS/)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc)

---

## 📄 License

MIT License

---

*Made with ❤️ by Vaibhav*
