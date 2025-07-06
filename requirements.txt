streamlit
# streamlit_app.py
import streamlit as st
import random
import os
from pathlib import Path

# Set page config
st.set_page_config(page_title="🎵 Emoji Song Guess Game", page_icon="🎶")

# Title
st.markdown("<h1 style='text-align: center; color: #ff3399;'>🎉 Emoji Song Guess 🎉</h1>", unsafe_allow_html=True)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.round = 0
    st.session_state.used_indexes = []
    st.session_state.correct_answer = None
    st.session_state.audio_file = None

# Game Data
emoji_song_data = [
    {"emojis": "👫💞🔗🎶", "answer": "belong together", "file": "Songs/Belong_Together.mp3"},
    {"emojis": "✍️⭐💫🚀", "answer": "rewrite the stars", "file": "Songs/Rewrite_the_stars.mp3"},
    {"emojis": "1💓 - Hindi", "answer": "phela pyar", "file": "Songs/Phela_Pyar.mp3"},
    {"emojis": "🍬❤️", "answer": "sweetheart", "file": "Songs/Sweetheart.mp3"},
    {"emojis": "🕵️💰My👧", "answer": "steal my girl", "file": "Songs/steal_my_girl.mp3"},
    {"emojis": "🌃🕰️🔁", "answer": "night changes", "file": "Songs/night_changes.mp3"},
    {"emojis": "🛣️🎒🚞🎶", "answer": "journey song", "file": "Songs/journey_song.mp3"},
    {"emojis": "💃🔥❤️🎤", "answer": "senorita", "file": "Songs/Senorita.mp3"},
    {"emojis": "Ajeeb⭕💭❓", "answer": "ajeeb o gareeb", "file": "Songs/ajeeb_o_gareeb.mp3"},
    {"emojis": "👧💃de -Hindi", "answer": "kudi nu nachne de", "file": "Songs/Kudi Nu Nachne de.mp3"}
]

# New question logic
def load_next_question():
    if st.session_state.round >= 10:
        st.success(f"🏁 Game Over! Your Score: {st.session_state.score} / 100")
        if st.button("🔁 Play Again"):
            st.session_state.score = 0
            st.session_state.round = 0
            st.session_state.used_indexes = []
            st.session_state.correct_answer = None
            st.experimental_rerun()
        return

    available_indexes = [i for i in range(len(emoji_song_data)) if i not in st.session_state.used_indexes]
    if available_indexes:
        index = random.choice(available_indexes)
        st.session_state.used_indexes.append(index)
        st.session_state.correct_answer = emoji_song_data[index]['answer']
        st.session_state.audio_file = emoji_song_data[index]['file']
        st.session_state.round += 1

# Load next question if first time or on correct guess
if st.session_state.correct_answer is None:
    load_next_question()

if st.session_state.round <= 10:
    st.markdown(f"### 🎵 Round {st.session_state.round} of 10")
    st.markdown(f"<h1 style='font-size: 60px; text-align: center'>{emoji_song_data[st.session_state.used_indexes[-1]]['emojis']}</h1>", unsafe_allow_html=True)

    user_guess = st.text_input("🔤 Enter Song Name:", "").strip().lower()

    if st.button("✅ Submit Guess"):
        if user_guess == st.session_state.correct_answer:
            st.session_state.score += 10
            st.success("🎉 Correct! Enjoy the song 🎶")

            audio_path = Path(st.session_state.audio_file)
            if audio_path.exists():
                audio_bytes = audio_path.read_bytes()
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning(f"Audio file not found: {audio_path}")

            # Load next question
            st.session_state.correct_answer = None
        else:
            st.error(f"❌ Wrong! The correct answer was: {st.session_state.correct_answer.title()}")
            st.session_state.correct_answer = None
