# import pandas as pd

# def load_data(path="data/processed/spotify_clean.csv"):
#     """Load cleaned Spotify data from CSV."""
#     return pd.read_csv(path)


# import pandas as pd
# import glob
# import os

# def load_data(path_pattern="spotify-dashboard/Spotify Account Data/StreamingHistory_*.json"):
#     """Load and clean Spotify streaming history from JSON files."""
    
#     # Find all matching files
#     files = glob.glob(path_pattern)
    
#     dfs = []
#     for f in files:
#         df = pd.read_json(f)
#         dfs.append(df)
    
#     # Combine all into one DataFrame
#     df = pd.concat(dfs, ignore_index=True)
    
#     # Rename columns to match dashboard
#     df = df.rename(columns={
#         "endTime": "played_at",
#         "artistName": "artist_name",
#         "trackName": "track_name",
#         "msPlayed": "ms_played"
#     })
    
#     # Add minutes_played for convenience
#     df["minutes_played"] = df["ms_played"] / 60000.0
    
#     # Add placeholder album column
#     df["album_name"] = "Unknown"
    
#     return df


# src/data_utils.py
import pandas as pd
import glob
import os
import json

def load_data(path_pattern="Spotify Account Data/StreamingHistory_music_*.json"):
    """Load and clean Spotify streaming history from JSON files."""

    files = glob.glob(path_pattern)

    if not files:
        raise FileNotFoundError(
            f"No Spotify history files found at {path_pattern}. "
            "Make sure your JSON files are inside 'Spotify Account Data/'."
        )

    dfs = []
    for f in files:
        with open(f, "r", encoding="utf-8") as infile:
            dfs.append(pd.DataFrame(json.load(infile)))

    # Combine into one DataFrame
    df = pd.concat(dfs, ignore_index=True)

    # Standardize column names
    df = df.rename(columns={
        "endTime": "played_at",
        "artistName": "artist_name",
        "trackName": "track_name",
        "msPlayed": "ms_played",
        # sometimes album data is included in extended exports
        "albumName": "album_name"
    })

    # If album_name not present, fill gracefully
    if "album_name" not in df.columns:
        df["album_name"] = "Unknown"

    # Add minutes_played for convenience
    df["minutes_played"] = df["ms_played"] / 60000.0

    return df
