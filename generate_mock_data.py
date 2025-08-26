# import pandas as pd
# import numpy as np
# import os

# # Make sure the folder exists
# os.makedirs("data/processed", exist_ok=True)

# np.random.seed(42)
# dates = pd.date_range("2024-01-01", periods=500, freq="6H")

# mock_data = {
#     "track_name": np.random.choice(
#         ["Song A", "Song B", "Song C", "Song D", "Song E"], size=len(dates)
#     ),
#     "artist_name": np.random.choice(
#         ["Artist X", "Artist Y", "Artist Z", "Artist W"], size=len(dates)
#     ),
#     "album_name": np.random.choice(["Album 1", "Album 2", "Album 3"], size=len(dates)),
#     "played_at": dates,
#     "ms_played": np.random.randint(30_000, 300_000, size=len(dates)),  # 30s–5min
# }

# df = pd.DataFrame(mock_data)
# df["minutes_played"] = df["ms_played"] / 60000

# # Save as proper CSV
# df.to_csv("data/processed/spotify_clean.csv", index=False)

# print("Mock data CSV created successfully!")
