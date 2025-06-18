import streamlit as st
from utils.fetch_news import fetch_top_headlines, fetch_news_by_query
from utils.summarize import summarize_article, translate_text
import tempfile
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer
import av
from gtts import gTTS
import base64

# ---------------- UI Setup ---------------- #
st.set_page_config(page_title="AI News Summarizer", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #FF4B4B;
            animation: fadeInDown 1s ease-in-out;
        }
        .summary-box {
            background-color: #1e1e1e;
            padding: 1.5em;
            border-radius: 10px;
            margin-bottom: 1em;
            box-shadow: 0 4px 14px rgba(255, 255, 255, 0.1);
        }
        .loader {
            border: 6px solid #f3f3f3;
            border-top: 6px solid #FF4B4B;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 Daily News Summarizer Bot</div>', unsafe_allow_html=True)
st.markdown("### Get short summaries of top news — by category, custom topic, or even voice!")

# ---------------- Voice Input Processor ---------------- #
class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame: av.AudioFrame):
        audio_data = frame.to_ndarray()
        try:
            audio = sr.AudioData(audio_data.tobytes(), frame.sample_rate, 2)
            text = self.recognizer.recognize_google(audio)
            st.session_state["query"] = text
            st.experimental_rerun()
        except sr.UnknownValueError:
            st.warning("Could not understand the voice input.")
        except sr.RequestError as e:
            st.error(f"Speech Recognition API error: {e}")

# ---------------- Input UI ---------------- #
col1, col2 = st.columns([3, 1])
with col1:
    query = st.text_input("🔍 Enter a topic (e.g., 'India crash', 'Israel Iran war')", st.session_state.get("query", ""))

with col2:
    st.markdown("### 🎙️ Speak")
    webrtc_streamer(
        key="speech",
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

category = st.selectbox("🗂️ Or choose a category:", [
    "general", "technology", "business", "entertainment", "health", "science", "sports"
])

# 🔤 Language Selection
language_map = {"English": "en", "Hindi": "hi", "Marathi": "mr"}
selected_lang = st.selectbox("🌐 Choose output language:", list(language_map.keys()))
lang_code = language_map[selected_lang]

# ---------------- gTTS Function ---------------- #
def play_audio(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_audio_path = fp.name
        tts.save(temp_audio_path)
        with open(temp_audio_path, "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        md = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"TTS error: {e}")

# ---------------- News Fetch + Summarize + Translate ---------------- #
if query.strip() or category:
    st.markdown('<div class="loader"></div>', unsafe_allow_html=True)
    with st.spinner("Fetching and summarizing news..."):
        articles = fetch_news_by_query(query) if query.strip() else fetch_top_headlines(category)

        if not articles:
            st.error("No news found. Try a different topic or category.")
        else:
            for idx, article in enumerate(articles):
                try:
                    summary = summarize_article(article)

                    if lang_code != "en":
                        translated_summary = translate_text(summary, dest_lang=lang_code)
                    else:
                        translated_summary = summary

                    st.markdown(f"""
                        <div class="summary-box">
                            <h4>🟢 News {idx + 1}</h4>
                            <p><b>Summary ({selected_lang}):</b> {translated_summary}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # TTS Player
                    with st.expander(f"🔊 Read News {idx + 1} Aloud"):
                        if st.button(f"🔈 Speak News {idx + 1}", key=f"tts_{idx}"):
                            play_audio(translated_summary, lang=lang_code)

                except Exception as e:
                    st.error(f"Error summarizing article {idx + 1}: {e}")
                    
