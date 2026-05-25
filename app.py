import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from src.spotify_client import (
    get_client,
    get_artist_by_name,
    get_artist_albums,
    get_album_tracks,
    search_album_spotify,
)


from src.song_service import build_song_object
from src.analytics import get_artist_summary
from src.spotify_artist_client import search_artist_spotify

from wordcloud import WordCloud

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(page_title="Song Analytics", page_icon="🎵", layout="wide")


# ======================
# AUTH
# ======================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    password = st.text_input("Enter access code", type="password")

    if password == st.secrets["APP_PASSWORD"]:
        st.session_state.authenticated = True
        st.rerun()

    elif password:
        st.error("Wrong password")

    st.stop()


# ======================
# TITLE
# ======================

st.title("🎵 Song Analytics Dashboard")


# ======================
# ARTIST CARD
# ======================


def render_artist_card(spotify_artist):

    if not spotify_artist:
        return

    st.subheader("🎧 Spotify Artist Profile")

    col1, col2 = st.columns([1, 2])

    with col1:
        if spotify_artist.get("image"):
            st.image(spotify_artist["image"], width=250)

    with col2:

        st.markdown(f"## {spotify_artist.get('name', 'Unknown')}")

        st.write(f"**Followers:** {spotify_artist.get('followers', 0):,}")

        popularity = spotify_artist.get("popularity", 0)

        st.write(f"**Popularity:** {popularity}/100")
        st.progress(popularity / 100)

        genres = spotify_artist.get("genres", [])
        if genres:
            st.write("**Genres:** " + ", ".join(genres[:5]))

        url = spotify_artist.get("spotify_url")
        if url:
            st.markdown(f"[Open Artist In Spotify]({url})")


# ======================
# SIDEBAR
# ======================

st.sidebar.header("Search")

artist_name = st.sidebar.text_input("Artist name")


if artist_name:

    # ----------------------
    # MUSICBRAINZ ARTIST
    # ----------------------
    artist = get_artist_by_name(artist_name)

    if not artist:
        st.warning("No artists found.")
        st.stop()

    # temp s
    sp = get_client()
    st.write("Spotify client OK:", sp is not None)
    # temp e
    # ----------------------
    # SPOTIFY ARTIST (SAFE)
    # ----------------------
    try:
        spotify_artist = search_artist_spotify(artist.get("name"))
    except Exception as e:
        st.error(f"Spotify error: {e}")
        spotify_artist = None

    st.write("Spotify artist loaded:", spotify_artist is not None)

    render_artist_card(spotify_artist)

    # ======================
    # RELEASES
    # ======================

    releases = get_artist_albums(artist["name"])

    releases = sorted(releases, key=lambda x: x.get("release_date", ""), reverse=True)

    # ======================
    # SUMMARY
    # ======================

    summary = get_artist_summary(releases)

    if summary:
        st.subheader("Artist Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Albums", summary["total_albums"])
        col2.metric("Oldest Release", summary["oldest_release"])
        col3.metric("Newest Release", summary["newest_release"])

    # ======================
    # TIMELINE
    # ======================

    st.subheader("Album Timeline")

    df = pd.DataFrame(releases)

    if not df.empty:

        df = df.dropna(subset=["release_date"])

        df["year"] = df["release_date"].astype(str).str[:4]

        year_counts = df["year"].value_counts().sort_index()

        fig, ax = plt.subplots()
        ax.plot(year_counts.index, year_counts.values, marker="o")
        ax.set_title("Albums per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Albums")

        st.pyplot(fig)

    # ======================
    # ALBUM SELECT
    # ======================

    st.subheader("Album Selection")

    album_map = {}

    for release in releases:
        label = f"{release.get('release_date')} | " f"{release.get('name')}"
        album_map[label] = release

    if not album_map:
        st.stop()

    selected_album = st.sidebar.selectbox("Choose an album", list(album_map.keys()))

    selected_release = album_map[selected_album]

    # ----------------------
    # SPOTIFY ALBUM
    # ----------------------
    try:
        spotify_album = search_album_spotify(
            artist.get("name"), selected_release.get("title")
        )
    except Exception as e:
        st.error(f"Spotify album error: {e}")
        spotify_album = None

    st.write("Spotify album loaded:", spotify_album is not None)

    if spotify_album and spotify_album.get("images"):
        st.image(spotify_album["images"][0]["url"], width=300)

    # ======================
    # TRACKS
    # ======================

    tracks = get_album_tracks(selected_release["id"])

    selected_song = None

    if tracks:

        song_titles = [t["name"] for t in tracks]

        selected_song = st.sidebar.selectbox("Choose a song", song_titles)

        st.write(f"Selected Song: {selected_song}")

    # ======================
    # SONG DATA
    # ======================

    if selected_song:

        song_data = build_song_object(artist.get("name"), selected_song)

        lyrics = song_data.get("lyrics")
        analytics = song_data.get("analytics")
        spotify = song_data.get("spotify")

        st.markdown("---")

        # ======================
        # SPOTIFY TRACK
        # ======================

        if spotify:

            st.subheader("🎵 Spotify Track")

            col1, col2 = st.columns([1, 2])

            with col1:
                if spotify.get("image"):
                    st.image(spotify["image"])

            with col2:

                st.write(f"**Album:** {spotify.get('album')}")

                popularity = spotify.get("popularity", 0)

                st.write(f"**Popularity:** {popularity}/100")
                st.progress(popularity / 100)

                if spotify.get("spotify_url"):
                    st.markdown(f"[Open Track In Spotify]({spotify['spotify_url']})")

        # ======================
        # LYRICS
        # ======================

        st.subheader("Lyrics")

        if lyrics:
            st.text_area("Lyrics", lyrics, height=400)
        else:
            st.info("Lyrics not found.")

        # ======================
        # ANALYTICS
        # ======================

        if analytics:

            st.subheader("Analytics")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Words", analytics["total_words"])
            col2.metric("Unique Words", analytics["unique_words"])
            col3.metric("Vocabulary %", analytics["richness"])

            # ======================
            # WORD CLOUD
            # ======================

            st.subheader("Word Cloud")

            words = lyrics.split()

            wordcloud = WordCloud(
                width=800, height=400, background_color="white"
            ).generate(" ".join(words))

            fig_wc, ax_wc = plt.subplots()

            ax_wc.imshow(wordcloud, interpolation="bilinear")
            ax_wc.axis("off")

            st.pyplot(fig_wc)
