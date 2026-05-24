import re
from collections import Counter


def calculate_basic_metrics(lyrics):

    lyrics = clean_text(lyrics)

    words = lyrics.split()

    total_words = len(words)

    unique_words = len(
        set(words)
    )

    richness = 0

    if total_words > 0:

        richness = round(
            unique_words
            / total_words
            * 100,
            2
        )

    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "richness": richness
    }


def get_top_words(
    lyrics,
    limit=10
):

    lyrics = clean_text(lyrics)

    words = lyrics.split()

    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "to",
        "of",
        "in",
        "on",
        "for",
        "is",
        "it",
        "that",
        "this",
        "i",
        "you",
        "my",
        "me"
    }

    filtered_words = [
        word
        for word in words
        if word not in stop_words
    ]

    counter = Counter(
        filtered_words
    )

    return counter.most_common(
        limit
    )



def clean_text(text):

    text = text.lower()

    text = re.sub(r"\[.*?\]", " ", text)
    text = re.sub(r"\(.*?\)", " ", text)

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text