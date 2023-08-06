# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import List, Union

try:
    import emoji

    has_emoji = True
except ImportError:
    has_emoji = False


def tokenize(
    text: str, max_ngram_length: int = 1, use_emoji: bool = True
) -> List[str]:
    """Convert a string to a list of lemmas."""
    converted_text: Union[str, List[str]] = text.lower()

    if has_emoji and use_emoji:
        parts = []
        highest_end = 0
        for emoji_part in emoji.emoji_list(text):
            parts += list(text[highest_end : emoji_part["match_start"]])
            parts.append(emoji_part["emoji"])
            highest_end = emoji_part["match_end"]
        parts += list(text[highest_end:])
        converted_text = [part for part in parts if part]

    tokens = [""]

    for char in converted_text:
        if char.isalpha() or char == "'":
            tokens[-1] += char
        elif has_emoji and emoji.is_emoji(char):
            tokens.append(char)
            tokens.append("")
        elif tokens[-1] != "":
            tokens.append("")

    tokens = [string for string in tokens if string]

    if max_ngram_length == 1:
        return tokens
    else:
        ngrams = []
        for ngram_length in range(1, max_ngram_length + 1):
            for index in range(len(tokens) + 1 - ngram_length):
                ngrams.append(" ".join(tokens[index : index + ngram_length]))
        return ngrams
