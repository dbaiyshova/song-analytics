import re


def calculate_basic_metrics(lyrics):

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        lyrics.lower()
    )

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