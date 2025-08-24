import pandas as pd

def load_data(path="data/processed/spotify_clean.csv"):
    """Load cleaned Spotify data from CSV."""
    return pd.read_csv(path)
