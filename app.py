import streamlit as st

from src.musicbrainz_client import (
    search_artist,
    get_artist_releases,
    get_release_tracks
)

from src.lyrics_client import get_lyrics


st.set_page_config(
    page_title="Song Analytics",
    page_icon="🎵"
)

st.title("🎵 Song Analytics")

artist_name = st.text_input(
    "Enter artist name"
)

if artist_name:

    data = search_artist(artist_name)

    artists = data.get("artists", [])

    if artists:

        artist = artists[0]

        st.subheader("Artist")

        st.write(
            f"**Name:** {artist.get('name')}"
        )

        artist_id = artist["id"]

        releases_data = get_artist_releases(
            artist_id
        )

        releases = [
            release
            for release in releases_data.get(
                "releases",
                []
            )
            if release.get("date")
        ]

        releases = sorted(
            releases,
            key=lambda x: x["date"]
        )

        st.subheader("Album Selection")

        album_map = {}

        for release in releases:

            title = release.get(
                "title",
                "Unknown"
            )

            date = release.get(
                "date",
                "Unknown"
            )

            label = f"{date} | {title}"

            album_map[label] = release

        selected_album = st.selectbox(
            "Choose an album",
            list(album_map.keys())
        )

        selected_release = album_map[
            selected_album
        ]

        track_data = get_release_tracks(
            selected_release["id"]
        )

        media = track_data.get(
            "media",
            []
        )

        tracks = []

        if media:
            tracks = media[0].get(
                "tracks",
                []
            )

        if tracks:

            song_titles = [
                track["title"]
                for track in tracks
            ]

        selected_song = st.selectbox(
            "Choose a song",
            song_titles
        )

        st.write(
            f"Selected Song: {selected_song}"
        )
        
        st.write(
            f"Selected Album: {selected_album}"
        )

        st.subheader("Lyrics")

        if tracks:

            lyrics = get_lyrics(
                artist.get("name"),
                selected_song
            )

            if lyrics:

                st.text_area(
                    "Lyrics",
                    lyrics,
                    height=400
                )

            else:

                st.info(
                    "Lyrics not found for this song."
                )

    else:
        st.warning(
            "No artists found."
        )