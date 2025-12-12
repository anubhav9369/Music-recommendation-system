# 🎵 Emotion-Aware Music Recommender

Emotion-Aware Music Recommender is an **NLP-powered web application** that detects emotions from text input and recommends Spotify playlists that align with the detected mood.  
This project combines **Natural Language Processing (NLP), Deep Learning, and Spotify API integration** to provide a personalized music recommendation experience.

💡 **Example:**  
*If you type “I feel lonely and sad today”, the model predicts **sadness** and recommends comforting playlists from Spotify.*

---

## ✨ Features

- 🧠 **Emotion Detection:** Fine-tuned Transformer model (GoEmotions categories + Neutral) classifies text into 27+ emotions.
- 🎶 **Music Recommendation:** Fetches Spotify playlists tailored to emotions using Spotipy.
- 🌐 **Interactive Web App:** Built with **Streamlit** for an intuitive user interface.
- 🚀 **Cloud Deployment:** Ready to deploy on **Render** or similar platforms.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **PyTorch** – Deep learning framework
- **Transformers (Hugging Face)** – Pretrained NLP models
- **Spotipy** – Spotify API wrapper
- **Streamlit** – Frontend interface
- **Flask** – (Optional) REST API for testing

---

## 📂 Project Structure

```

NLP Project/
│-- emotion_model/ # Saved fine-tuned Transformer model
│-- integrate.py # Streamlit app (main entry point)
│-- music.py # Spotify playlist recommender class
│-- requirements.txt # Project dependencies
│-- .gitignore # Ignore unnecessary files
│-- README.md # Project documentation

```

---

## ⚙️ Installation

1. **Clone the Repository**

git clone https://github.com/your-username/emotion-aware-music-recommender.git
cd emotion-aware-music-recommender


2. **Create Virtual Environment**

```
python -m venv emotion_env
```

   - **On Windows**
   
   ```
   emotion_env\Scripts\activate
   ```
   
   - **On Mac/Linux**
   
   ```
   source emotion_env/bin/activate
   ```

3. **Install Dependencies**

```
pip install -r requirements.txt
```

4. **Spotify API Setup**
- Create a Spotify Developer Account: https://developer.spotify.com
- Get your Client ID and Client Secret.
- Store them in a `.env` file **or** configure as environment variables on Render.

---

## ▶️ Usage

**Run the Streamlit app locally:**

streamlit run integrate.py

Then visit [http://localhost:8501](http://localhost:8501) in your browser.

**Example Input/Output:**
- Input: “I am so excited today!”
- Predicted Emotion: Excitement
- Suggested Playlist: High Energy Boost + matching Spotify playlists

---

## ☁️ Deployment on Render

1. Push your repository to GitHub.
2. Go to Render → New Web Service.
3. Connect your repo.
4. Configure:
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     streamlit run integrate.py --server.port $PORT --server.address 0.0.0.0
     ```
   - **Add Environment Variables:**
     - SPOTIPY_CLIENT_ID
     - SPOTIPY_CLIENT_SECRET
     - SPOTIPY_REDIRECT_URI

Render will build and deploy your app! 🚀

---

## 📊 Supported Emotions

The model predicts emotions from the GoEmotions dataset plus Neutral, including:

`admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral`

---

## 📸 Screenshots / Demo

*Add screenshots of your app UI here after running locally or on the deployed version.*

Example placeholders:
- Home Screen
- Emotion Prediction Example
- Playlist Recommendations

---

## 🤝 Contributors

- **Suman Giri** (Lead Developer, NLP & Integration)
- **P V Akhila** (Spotify API Integration & Deployment)
- **Anubhav Verma** (Model Training & Dataset Processing)

---

## 📜 License

This project is licensed under the MIT License – feel free to use, modify, and share.

---

**With this project, we bridge AI + Music, making technology more human-centered and emotionally aware.**


