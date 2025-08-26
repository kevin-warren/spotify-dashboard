import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_utils import load_data
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Spotify Dashboard", page_icon="🎵")
st.title("🎵 Spotify Listening Dashboard")

# Load data
df = load_data()

# Preprocess
df['played_at'] = pd.to_datetime(df['played_at'])
df['hour'] = df['played_at'].dt.hour
df['day_of_week'] = df['played_at'].dt.day_name()
df = df[df['track_name'] != 'Unknown Track']
df = df[df['artist_name'] != 'Unknown Artist']

# --- SUMMARY STATS SECTION ---
st.header("Summary Statistics")

# total listening time in hours
total_minutes = df['ms_played'].sum() / 60000
total_hours = total_minutes / 60

# number of unique songs and artists
unique_tracks = df['track_name'].nunique()
unique_artists = df['artist_name'].nunique()

# average listening session length (per day)
df['date'] = df['played_at'].dt.date
daily_minutes = df.groupby('date')['ms_played'].sum() / 60000
avg_session = np.mean(daily_minutes)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Hours", f"{total_hours:.1f}")
col2.metric("Unique Tracks", unique_tracks)
col3.metric("Unique Artists", unique_artists)
col4.metric("Avg Daily Minutes", f"{avg_session:.1f}")



# --- INTERACTIVE FILTERS ---
st.header("Listening History by Song and Artist")

# Artist filter
artist_list = df['artist_name'].dropna().unique()
artist_choice = st.selectbox("Select an Artist:", options=["All"] + sorted(artist_list.tolist()))

filtered_df = df.copy()
if artist_choice != "All":
    filtered_df = filtered_df[filtered_df['artist_name'] == artist_choice]

# Track filter (depends on artist filter)
track_list = filtered_df['track_name'].dropna().unique()
track_choice = st.selectbox("Select a Track:", options=["All"] + sorted(track_list.tolist()))

if track_choice != "All":
    filtered_df = filtered_df[filtered_df['track_name'] == track_choice]

st.write(f"🎶 Showing {len(filtered_df)} plays")

# --- Chart: Listening time over time ---


# Group listening by day
daily_df = (
    filtered_df
    .groupby(filtered_df['played_at'].dt.to_period("D"))
    .sum(numeric_only=True)['minutes_played']
    .reset_index()
)

# Convert Period -> Timestamp for Altair
daily_df['date'] = daily_df['played_at'].dt.to_timestamp()
daily_df = daily_df.rename(columns={'minutes_played': 'Minutes Listened'})

# Altair line chart
chart = (
    alt.Chart(daily_df)
    .mark_line(point=True)
    .encode(
        x=alt.X('date:T', title="Date"),
        y=alt.Y('Minutes Listened:Q', title="Minutes Listened"),
        tooltip=['date:T', 'Minutes Listened:Q']
    )
    .properties(
        title="Listening Time Over Time",
        width=700,
        height=400
    )
)

st.altair_chart(chart, use_container_width=True)




import altair as alt

# --- TOP ARTISTS SECTION ---
st.header("🎵 Top Artists")
top_artists = df['artist_name'].value_counts().head(10).reset_index()
top_artists.columns = ['Artist', 'Plays']

chart_artists = (
    alt.Chart(top_artists)
    .mark_bar()
    .encode(
        x=alt.X('Plays:Q', title="Number of Plays"),
        y=alt.Y('Artist:N', sort='-x', title="Artist"),
        tooltip=['Artist', 'Plays']
    )
    .properties(width=700, height=400, title="Top 10 Artists")
)
st.altair_chart(chart_artists, use_container_width=True)

# --- TOP TRACKS SECTION ---
st.header("🎵 Top Tracks")
top_tracks = df['track_name'].value_counts().head(10).reset_index()
top_tracks.columns = ['Track', 'Plays']

chart_tracks = (
    alt.Chart(top_tracks)
    .mark_bar()
    .encode(
        x=alt.X('Plays:Q', title="Number of Plays"),
        y=alt.Y('Track:N', sort='-x', title="Track"),
        tooltip=['Track', 'Plays']
    )
    .properties(width=700, height=400, title="Top 10 Tracks")
)
st.altair_chart(chart_tracks, use_container_width=True)

# --- LISTENING BY DAY SECTION ---
st.header("🎵 Listening by Day")
listening_by_day = df.groupby('day_of_week')['minutes_played'].sum().reset_index()
listening_by_day.columns = ['Day of Week', 'Minutes Played']

chart_day = (
    alt.Chart(listening_by_day)
    .mark_bar()
    .encode(
        x=alt.X('Day of Week:N', title="Day of the Week", sort=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']),
        y=alt.Y('Minutes Played:Q', title="Minutes Played"),
        tooltip=['Day of Week', 'Minutes Played']
    )
    .properties(width=700, height=400, title="Listening by Day of Week")
)
st.altair_chart(chart_day, use_container_width=True)

# --- TOP ALBUMS SECTION ---
# st.header("🎵 Top Albums")
# top_albums = df['album_name'].value_counts().head(10).reset_index()
# top_albums.columns = ['Album', 'Plays']

# chart_albums = (
#     alt.Chart(top_albums)
#     .mark_bar()
#     .encode(
#         x=alt.X('Plays:Q', title="Number of Plays"),
#         y=alt.Y('Album:N', sort='-x', title="Album"),
#         tooltip=['Album', 'Plays']
#     )
#     .properties(width=700, height=400, title="Top 10 Albums")
# )
# st.altair_chart(chart_albums, use_container_width=True)

# # --- TOP GENRES SECTION ---
# st.header("🎵 Top Genres")
# top_genres = df['genre'].value_counts().head(10)
# st.bar_chart(top_genres)
