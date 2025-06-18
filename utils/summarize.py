# summarize.py (using gemini-1.5-flash-latest ✅)

import os
from dotenv import load_dotenv
import google.generativeai as genai
from gtts import gTTS
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_article(article):
    """
    Summarize a news article using Gemini API.
    """
    title = article.get("title", "")
    content = article.get("content") or article.get("description") or ""

    prompt = f"Summarize this news article in 3 lines:\n\nTitle: {title}\n\nContent: {content}"

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini summarization failed: {e}"

def translate_text(text, dest_lang="hi"):
    """
    Translate text to the specified language using deep-translator.
    dest_lang: 'hi' for Hindi, 'mr' for Marathi
    """
    try:
        translated = GoogleTranslator(source='auto', target=dest_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation failed: {e}"

def text_to_speech(text, lang="en", filename="summary.mp3"):
    """
    Convert text to speech and save as an mp3 file.
    lang: 'en' for English, 'hi' for Hindi, 'mr' for Marathi
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return filename
    except Exception as e:
        return f"TTS failed: {e}"

# Example usage
if __name__ == "__main__":
    # Example article dictionary
    article = {
        "title": "India launches new satellite",
        "content": "The Indian Space Research Organisation (ISRO) has successfully launched a new communication satellite into orbit. The satellite will provide improved telecommunication and broadcasting services across the country."
    }

    # Summarize
    summary = summarize_article(article)
    print("Summary (English):", summary)

    # Translate to Hindi
    hindi_summary = translate_text(summary, dest_lang="hi")
    print("Summary (Hindi):", hindi_summary)

    # Translate to Marathi
    marathi_summary = translate_text(summary, dest_lang="mr")
    print("Summary (Marathi):", marathi_summary)

    # TTS for Hindi summary
    tts_file_hi = text_to_speech(hindi_summary, lang="hi", filename="summary_hi.mp3")
    print("Hindi TTS file saved as:", tts_file_hi)

    # TTS for Marathi summary
    tts_file_mr = text_to_speech(marathi_summary, lang="mr", filename="summary_mr.mp3")
    print("Marathi TTS file saved as:", tts_file_mr)
