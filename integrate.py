import streamlit as st
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from music import SpotifyEmotionPlaylistRecommender 
import os
from dotenv import load_dotenv

load_dotenv() 

# Load Emotion Model
@st.cache_resource
def load_model():
    model_path = model_path = "/Users/anubhavverma/Downloads/NLP Project/emotion_model"  # change if needed
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    return model, tokenizer, device

model, tokenizer, device = load_model()

label_mapping = {
    0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance", 4: "approval",
    5: "caring", 6: "confusion", 7: "curiosity", 8: "desire", 9: "disappointment",
    10: "disapproval", 11: "disgust", 12: "embarrassment", 13: "excitement",
    14: "fear", 15: "gratitude", 16: "grief", 17: "joy", 18: "love",
    19: "nervousness", 20: "optimism", 21: "pride", 22: "realization",
    23: "relief", 24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
}
label_names = list(label_mapping.values())


def predict_emotion(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    pred = np.argmax(outputs.logits.detach().cpu().numpy(), axis=1)[0]
    return label_names[pred]


# -----------------------
# Load Spotify Recommender
# -----------------------
@st.cache_resource
def load_spotify():
    client_id = "112c1e4119734226aa7a46691dd18604"
    client_secret = "6bf8845b9dea432181a2b11a5deae0a9"
    redirect_uri = "http://127.0.0.1:8000/callback"
    return SpotifyEmotionPlaylistRecommender(client_id, client_secret, redirect_uri)

spotify_recommender = load_spotify()


# -----------------------
# Streamlit UI
# -----------------------
st.title("🎵 Emotion-Aware Music Recommender")
st.write("Tell me how you're feeling, and I'll recommend a Spotify playlist for you 💡")

# Ask user input
user_text = st.text_area("💬 How are you feeling today?", "")

if st.button("Get Playlist"):
    if user_text.strip():
        # Step 1: Predict emotion
        predicted_emotion = predict_emotion(user_text)
        st.success(f"Detected Emotion: **{predicted_emotion}**")

        # Step 2: Recommend playlist
        recommendation = spotify_recommender.recommend_spotify_playlist(predicted_emotion)

        st.subheader("🎶 Recommended Playlist")
        st.write(f"**{recommendation['name']}**")
        st.write(recommendation["description"])

        if recommendation["spotify_playlists"]:
            for i, playlist in enumerate(recommendation["spotify_playlists"], 1):
                st.markdown(f"**{i}. {playlist['name']}** by {playlist['owner']}")
                st.write(f"Tracks: {playlist['total_tracks']}")
                st.markdown(f"[Open in Spotify]({playlist['external_url']})")
        else:
            st.warning("No Spotify playlists found for this emotion.")
    else:
        st.error("Please type how you are feeling.")
