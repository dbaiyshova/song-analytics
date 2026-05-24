import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.musicbrainz_client import (
    search_artist,
    get_artist_releases,
    get_release_tracks
)

from src.song_service import build_song_object

from src.analytics import get_artist_summary

from wordcloud import WordCloud


# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="Song Analytics",
    page_icon="🎵"
)


# ======================
# AUTH (SECURITY)
# ======================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


if not st.session_state.authenticated:

    password = st.text_input(
        "Enter access code",
        type="password"
    )

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
# SIDEBAR INPUT
# ======================

st.sidebar.header("Search")

artist_name = st.sidebar.text_input("Artist name")


if artist_name:

    data = search_artist(artist_name)

    artists = data.get("artists", [])

    if not artists:
        st.warning("No artists found.")
        st.stop()

    artist = artists[0]

    st.subheader("Artist Overview")

    st.write(f"**Name:** {artist.get('name')}")


    # ======================
    # RELEASES
    # ======================

    artist_id = artist["id"]

    releases_data = get_artist_releases(artist_id)

    releases = [
        r for r in releases_data.get("releases", [])
        if r.get("date")
    ]

    releases = sorted(releases, key=lambda x: x["date"])


    # ======================
    # ARTIST SUMMARY
    # ======================

    summary = get_artist_summary(releases)

    if summary:

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Albums", summary["total_albums"])
        col2.metric("Oldest Release", summary["oldest_release"])
        col3.metric("Newest Release", summary["newest_release"])


    # ======================
    # ALBUM TIMELINE
    # ======================

    st.subheader("Album Timeline")

    df = pd.DataFrame(releases)

    df = df.dropna(subset=["date"])

    df["year"] = df["date"].str[:4]

    year_counts = df["year"].value_counts().sort_index()

    fig, ax = plt.subplots()

    ax.plot(
        year_counts.index,
        year_counts.values,
        marker="o"
    )

    ax.set_title("Albums per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Albums")

    st.pyplot(fig)


    # ======================
    # ALBUM SELECTION
    # ======================

    st.subheader("Album Selection")

    album_map = {}

    for release in releases:

        label = f"{release.get('date')} | {release.get('title')}"
        album_map[label] = release

    selected_album = st.sidebar.selectbox(
        "Choose an album",
        list(album_map.keys())
    )

    selected_release = album_map[selected_album]


    # ======================
    # TRACKS
    # ======================

    track_data = get_release_tracks(selected_release["id"])

    media = track_data.get("media", [])

    tracks = []

    if media:
        tracks = media[0].get("tracks", [])


    # ======================
    # SONG SELECTION
    # ======================

    selected_song = None

    if tracks:

        song_titles = [t["title"] for t in tracks]

        selected_song = st.sidebar.selectbox(
            "Choose a song",
            song_titles
        )

        st.write(f"Selected Song: {selected_song}")


    # ======================
    # SONG ENGINE (UNIFIED LAYER)
    # ======================

    if selected_song:

        song_data = build_song_object(
            artist.get("name"),
            selected_song
        )

        lyrics = song_data["lyrics"]
        analytics = song_data["analytics"]
        spotify = song_data["spotify"]


        # ======================
        # LYRICS
        # ======================

        st.markdown("---")
        st.subheader("Lyrics")

        if lyrics:

            st.text_area(
                "Lyrics",
                lyrics,
                height=400
            )

        else:
            st.info("Lyrics not found for this song.")


        # ======================
        # SPOTIFY INFO
        # ======================

        if spotify:

            st.subheader("Spotify Info")

            if spotify.get("image"):
                st.image(spotify["image"])

            popularity = spotify.get(
                "popularity",
                0
            )

            st.write(
                f"**Popularity:** {popularity}/100"
            )

            st.progress(
                popularity / 100
            )


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
                width=800,
                height=400,
                background_color="white"
            ).generate(" ".join(words))

            fig_wc, ax_wc = plt.subplots()

            ax_wc.imshow(wordcloud, interpolation="bilinear")
            ax_wc.axis("off")

            st.pyplot(fig_wc)