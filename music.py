import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

class SpotifyEmotionPlaylistRecommender:
    def __init__(self, client_id, client_secret, redirect_uri):
        """
        Initialize the Spotify playlist recommender
        """
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="playlist-read-private,user-read-private"
            ))
        except Exception as e:
            print(f"Error initializing Spotify client: {e}")
            self.sp = None

        # ✅ Expanded mapping for 27+ emotions
        self.emotion_to_playlist = {
            "admiration": {"name": "Inspiring Vibes", "description": "Music that fuels admiration and awe", "energy": 0.6, "valence": 0.8},
            "amusement": {"name": "Fun & Laughter", "description": "Playful tracks to keep the mood light", "energy": 0.8, "valence": 0.9},
            "anger": {"name": "Calm & Release", "description": "Relaxing songs to cool down anger", "energy": 0.3, "valence": 0.4},
            "annoyance": {"name": "Peaceful Reset", "description": "Soothing sounds to reduce irritation", "energy": 0.4, "valence": 0.5},
            "approval": {"name": "Positive Affirmations", "description": "Uplifting music for encouragement", "energy": 0.7, "valence": 0.8},
            "caring": {"name": "Warm & Caring", "description": "Gentle songs full of kindness", "energy": 0.5, "valence": 0.7},
            "confusion": {"name": "Focus Flow", "description": "Tracks to clear your head", "energy": 0.5, "valence": 0.6},
            "curiosity": {"name": "Discover & Explore", "description": "Eclectic tracks for curious minds", "energy": 0.7, "valence": 0.8},
            "desire": {"name": "Passion Waves", "description": "Romantic and passionate songs", "energy": 0.7, "valence": 0.8},
            "disappointment": {"name": "Healing Tones", "description": "Comforting tracks to lift your spirit", "energy": 0.3, "valence": 0.4},
            "disapproval": {"name": "Reset & Recharge", "description": "Balanced tracks to stabilize emotions", "energy": 0.4, "valence": 0.5},
            "disgust": {"name": "Clean Slate", "description": "Refreshing sounds to shake off negativity", "energy": 0.5, "valence": 0.6},
            "embarrassment": {"name": "Confidence Boost", "description": "Empowering tracks to lift self-esteem", "energy": 0.7, "valence": 0.7},
            "excitement": {"name": "High Energy Boost", "description": "Hype tracks to fuel excitement", "energy": 0.9, "valence": 0.9},
            "fear": {"name": "Safe & Secure", "description": "Comforting songs to ease fears", "energy": 0.3, "valence": 0.5},
            "gratitude": {"name": "Thankful Vibes", "description": "Songs of appreciation and joy", "energy": 0.7, "valence": 0.9},
            "grief": {"name": "Gentle Healing", "description": "Emotional tracks for grieving hearts", "energy": 0.2, "valence": 0.3},
            "joy": {"name": "Pure Happiness", "description": "Upbeat songs for joyful moods", "energy": 0.9, "valence": 0.95},
            "love": {"name": "Romantic Tunes", "description": "Heartfelt love songs", "energy": 0.7, "valence": 0.9},
            "nervousness": {"name": "Calm Focus", "description": "Tracks to ease nervous energy", "energy": 0.4, "valence": 0.6},
            "optimism": {"name": "Bright Future", "description": "Hopeful and cheerful music", "energy": 0.8, "valence": 0.9},
            "pride": {"name": "Victory Anthems", "description": "Empowering tracks to celebrate wins", "energy": 0.8, "valence": 0.8},
            "realization": {"name": "Lightbulb Moments", "description": "Reflective tracks for clarity", "energy": 0.6, "valence": 0.7},
            "relief": {"name": "Breathe Easy", "description": "Relaxing music for relief", "energy": 0.4, "valence": 0.7},
            "remorse": {"name": "Forgiveness & Growth", "description": "Soothing tracks for self-healing", "energy": 0.3, "valence": 0.4},
            "sadness": {"name": "Soft Comfort", "description": "Gentle emotional tracks", "energy": 0.2, "valence": 0.3},
            "surprise": {"name": "Unexpected Joys", "description": "Eclectic tracks for surprising moods", "energy": 0.7, "valence": 0.8},
            "neutral": {"name": "Everyday Flow", "description": "Balanced tracks for any mood", "energy": 0.5, "valence": 0.5}
        }

        # ✅ Search terms for Spotify queries
        self.emotion_search_terms = {
            "admiration": "inspirational music",
            "amusement": "fun upbeat playlist",
            "anger": "calm relaxing music",
            "annoyance": "chill peace vibes",
            "approval": "positive uplifting",
            "caring": "kind gentle tracks",
            "confusion": "focus concentration",
            "curiosity": "eclectic discovery music",
            "desire": "romantic passion songs",
            "disappointment": "comfort emotional healing",
            "disapproval": "neutral focus calm",
            "disgust": "fresh reset cleanse music",
            "embarrassment": "confidence empowerment",
            "excitement": "high energy workout party",
            "fear": "comfort secure calm",
            "gratitude": "thankful appreciation vibes",
            "grief": "healing emotional piano",
            "joy": "happy upbeat feel good",
            "love": "romantic love songs",
            "nervousness": "calm meditation focus",
            "optimism": "bright cheerful happy",
            "pride": "victory anthems celebration",
            "realization": "reflective calm discovery",
            "relief": "relax chill unwind",
            "remorse": "forgiveness emotional",
            "sadness": "sad melancholic emotional",
            "surprise": "unexpected eclectic playlist",
            "neutral": "focus concentration study"
        }

    def search_spotify_playlists(self, query, limit=5):
        if not self.sp:
            print("Spotify client not initialized")
            return []

        try:
            results = self.sp.search(q=query, type='playlist', limit=limit)
            playlists = []

            if not results or 'playlists' not in results or 'items' not in results['playlists']:
                return playlists

            for item in results['playlists']['items']:
                if item is None:
                    continue
                playlist = {
                    'name': item.get('name', 'Unknown Playlist'),
                    'description': item.get('description', 'No description available'),
                    'uri': item.get('uri', ''),
                    'external_url': item.get('external_urls', {}).get('spotify', ''),
                    'owner': item.get('owner', {}).get('display_name', 'Unknown'),
                    'total_tracks': item.get('tracks', {}).get('total', 0)
                }
                playlists.append(playlist)
            return playlists
        except Exception as e:
            print(f"Error searching Spotify playlists: {e}")
            return []

    def recommend_spotify_playlist(self, emotion):
        emotion = emotion.lower()
        if emotion not in self.emotion_to_playlist:
            emotion = "neutral"

        playlist_info = self.emotion_to_playlist[emotion].copy()
        search_query = self.emotion_search_terms.get(emotion, "focus")
        spotify_playlists = self.search_spotify_playlists(search_query)

        playlist_info["spotify_playlists"] = spotify_playlists
        return playlist_info


if __name__ == "__main__":
    client_id = "112c1e4119734226aa7a46691dd18604"
    client_secret = "6bf8845b9dea432181a2b11a5deae0a9"
    redirect_uri = "http://127.0.0.1:8000/callback"

    try:
        spotify_recommender = SpotifyEmotionPlaylistRecommender(client_id, client_secret, redirect_uri)

        # ✅ GoEmotions categories + neutral
        emotions = ["admiration", "amusement", "anger", "annoyance", "approval", "caring",
                    "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust",
                    "embarrassment", "excitement", "fear", "gratitude", "grief", "joy", "love",
                    "nervousness", "optimism", "pride", "realization", "relief", "remorse",
                    "sadness", "surprise", "neutral"]

        for emotion in emotions:
            print(f"\n=== Recommendation for {emotion} ===")
            recommendation = spotify_recommender.recommend_spotify_playlist(emotion)

            print(f"Playlist Name: {recommendation['name']}")
            print(f"Description: {recommendation['description']}")

            if recommendation['spotify_playlists']:
                print("Spotify Playlists:")
                for i, playlist in enumerate(recommendation['spotify_playlists'], 1):
                    print(f"{i}. {playlist['name']} by {playlist['owner']}")
                    print(f"   Tracks: {playlist['total_tracks']}")
                    print(f"   URL: {playlist['external_url']}\n")
            else:
                print("No Spotify playlists found for this emotion")

    except Exception as e:
        print(f"Error in main execution: {e}")
