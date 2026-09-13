import json
from pathlib import Path

import pandas as pd

raw_data_dir = Path("data/raw")
processed_data_dir = Path("data/processed")

processed_data_dir.mkdir(parents=True, exist_ok=True)

time_ranges = ["short_term", "medium_term", "long_term"]

# --------------------
# Process artist data
# --------------------

artist_rows = []

for time_range in time_ranges:
    input_file = raw_data_dir / f"top_artists_{time_range}.json"
    
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        
    for rank, artist in enumerate(data["items"], start=1):
        artist_rows.append(
            {
                "time_range": time_range,
                "rank": rank,
                "artist_name": artist["name"],
                "spotify_id": artist["id"],
                "spotify_uri": artist["uri"],
                "spotify_url": artist["external_urls"]["spotify"],
            }
            
        )
        
artists_df = pd.DataFrame(artist_rows)

output_file = processed_data_dir / "top_artists.csv"
artists_df.to_csv(output_file, index=False)

print(f"Saved {output_file}")
print(artists_df.head())

# --------------------
# Process track data
# --------------------

track_rows = []

for time_range in time_ranges:
    input_file = raw_data_dir / f"top_tracks_{time_range}.json"
    
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        
    for rank, track in enumerate(data["items"], start=1):
        track_rows.append(
            {
                "time_range": time_range,
                "rank": rank,
                "track_name": track["name"],
                "track_id": track["id"],
                "artist_names": ", ".join(
                    artist["name"] for artist in track["artists"]
                ),
                "album_name": track["album"]["name"],
                "album_release_date": track["album"]["release_date"],
                "duration_ms": track["duration_ms"],
                "explicit": track["explicit"],
                "isrc": track["external_ids"].get("isrc"),
                "spotify_url": track["external_urls"]["spotify"],
                "album_image_url": (
                    track["album"]["images"][0]["url"]
                    if track ["album"]["images"]
                    else None
                ),
            }
        )
        
tracks_df = pd.DataFrame(track_rows)

output_file = processed_data_dir / "top_tracks.csv"
tracks_df.to_csv(output_file, index=False)

print(f"Saved {output_file}")
print(tracks_df.head())