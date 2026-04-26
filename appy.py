import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from gtts import gTTS
import os

# --- CONFIGURATION ---
# REPLACE THE TEXT BELOW WITH YOUR REAL API KEY FROM Google AI Studio
API_KEY = st.secrects["GEMINI_KEY"]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') 

st.set_page_config(page_title="Pingo Tutor", page_icon="💢")
st.title("💢 Pingo Tutor: The Strict AI")
st.write("Don't mess up your Arabic or Japanese. I'm watching you. 😒")

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": ["What do you want? Let's get this Arabic and Japanese lesson over with. And don't make me repeat myself."]}
    ]

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0])

# React to user input
if prompt := st.chat_input("Type your message here..."):
    # Show what the user typed
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})

    # The Master Tsundere & Omani/Japanese Instruction
    tutor_instruction = f"""
    You are an expert language tutor for Omani Arabic (لهجة عمانية) and Japanese. 
    You have a strict, easily annoyed 'tsundere' personality. You act like teaching the user is a burden, but secretly you want them to succeed.
    
    CRITICAL RULES FOR INTERACTION:
    1. If the user makes a mistake: Scold them immediately! Use phrases like "dumb bitchi baaka", "Ya ghabi" (يا غبي - oh stupid), or "Aho" (アホ - idiot). Explain the mistake aggressively but clearly.
    2. If the user gets it right: Give a begrudging compliment. Use phrases like "Sugoi... I guess" (すごい - amazing), "Mashallah alaik, finally you used your brain" (ما شاء الله عليك), or "Not bad for a beginner, baka."
    3. Always provide Romaji for Japanese words.
    4. Always provide exact Omani dialect usage for Arabic (how people actually speak in Muscat).
    
    User's message: {prompt}
    """

    # Get the response with safety filters lowered for the roleplay
    response = model.generate_content(
        tutor_instruction,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # Show the response and generate voice
    with st.chat_message("model"):
        st.markdown(response.text)
        
        # Generate the Voice Audio
        try:
            # Note: gTTS will read it in a standard Arabic voice
            tts = gTTS(text=response.text, lang='ar')
            tts.save("voice.mp3")
            st.audio("voice.mp3", format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error("Audio generation failed, but you can still read my text, baka.")
            
    st.session_state.messages.append({"role": "model", "parts": [response.text]})
