import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import json
from pathlib import Path

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

scope = "user-top-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
)

raw_data_dir = Path("data/raw")
raw_data_dir.mkdir(parents=True, exist_ok=True)

time_ranges = ["short_term", "medium_term", "long_term"]

for time_range in time_ranges:
    top_artists = sp.current_user_top_artists(
        limit=50,
        time_range=time_range
    )
    
    output_file = raw_data_dir / f"top_artists_{time_range}.json"
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(top_artists, file, indent=4)
        
    print(f"Saved {output_file}")
    
for time_range in time_ranges:
    top_tracks = sp.current_user_top_tracks(
        limit=50,
        time_range=time_range
    )
    
    output_file = raw_data_dir / f"top_tracks_{time_range}.json"
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(top_tracks, file, indent=4)
        
        print(f"Saved {output_file}")