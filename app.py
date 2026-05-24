import streamlit as st

from src.musicbrainz_client import (
    search_artist,
    get_artist_releases
)

from src.lyrics_client import get_lyrics


#imports

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

        releases = releases_data.get(
            "releases",
            []
        )

        st.subheader("Releases")

        for release in releases[:20]:

            title = release.get(
                "title",
                "Unknown"
            )

            date = release.get(
                "date",
                "Unknown"
            )

            st.write(
                f"• {title} ({date})"
            )

    else:
        st.warning(
            "No artists found."
        )
    
    st.subheader("Lyrics Test")

    lyrics = get_lyrics(
    artist.get("name"),
    "Yellow"
    )

    if lyrics:
        st.text_area(
            "Lyrics",
            lyrics[:2000],
            height=300
        )
    else:
        st.info(
            "Lyrics not found."
        )




