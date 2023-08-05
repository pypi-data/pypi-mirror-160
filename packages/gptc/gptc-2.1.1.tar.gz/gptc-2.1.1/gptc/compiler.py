# SPDX-License-Identifier: LGPL-3.0-or-later

import gptc.tokenizer
from typing import Iterable, Mapping, List, Dict, Union

WEIGHTS_T = List[int]
CONFIG_T = Union[List[str], int, str]
MODEL = Dict[str, Union[WEIGHTS_T, CONFIG_T]]


def compile(
    raw_model: Iterable[Mapping[str, str]], max_ngram_length: int = 1
) -> MODEL:
    """Compile a raw model.

    Parameters
    ----------
    raw_model : list of dict
        A raw GPTC model.

    max_ngram_length : int
        Maximum ngram lenght to compile with.

    Returns
    -------
    dict
        A compiled GPTC model.

    """

    categories: Dict[str, List[str]] = {}

    for portion in raw_model:
        text = gptc.tokenizer.tokenize(portion["text"], max_ngram_length)
        category = portion["category"]
        try:
            categories[category] += text
        except KeyError:
            categories[category] = text

    categories_by_count: Dict[str, Dict[str, float]] = {}

    names = []

    for category, text in categories.items():
        if not category in names:
            names.append(category)

        categories_by_count[category] = {}
        for word in text:
            try:
                categories_by_count[category][word] += 1 / len(
                    categories[category]
                )
            except KeyError:
                categories_by_count[category][word] = 1 / len(
                    categories[category]
                )
    word_weights: Dict[str, Dict[str, float]] = {}
    for category, words in categories_by_count.items():
        for word, value in words.items():
            try:
                word_weights[word][category] = value
            except KeyError:
                word_weights[word] = {category: value}

    model: MODEL = {}
    for word, weights in word_weights.items():
        total = sum(weights.values())
        new_weights: List[int] = []
        for category in names:
            new_weights.append(
                round((weights.get(category, 0) / total) * 65535)
            )
        model[word] = new_weights

    model["__names__"] = names
    model["__ngrams__"] = max_ngram_length
    model["__version__"] = 3
    model["__emoji__"] = int(tokenizer.has_emoji)

    return model
