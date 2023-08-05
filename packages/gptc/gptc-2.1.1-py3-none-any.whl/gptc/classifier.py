# SPDX-License-Identifier: LGPL-3.0-or-later

import gptc.tokenizer, gptc.compiler, gptc.exceptions, gptc.weighting, gptc.model_info
import warnings
from typing import Dict, Union, cast, List


class Classifier:
    """A text classifier.

    Parameters
    ----------
    model : dict
        A compiled GPTC model.

    max_ngram_length : int
        The maximum ngram length to use when tokenizing input. If this is
        greater than the value used when the model was compiled, it will be
        silently lowered to that value.

    Attributes
    ----------
    model : dict
        The model used.

    """

    def __init__(self, model: gptc.compiler.MODEL, max_ngram_length: int = 1):
        if model.get("__version__", 0) != 3:
            raise gptc.exceptions.UnsupportedModelError(
                f"unsupported model version"
            )
        self.model = model
        model_ngrams = cast(int, model.get("__ngrams__", 1))
        self.max_ngram_length = min(max_ngram_length, model_ngrams)
        self.has_emoji = (
            gptc.tokenizer.has_emoji and gptc.model_info.model_has_emoji(model)
        )

    def confidence(self, text: str) -> Dict[str, float]:
        """Classify text with confidence.

        Parameters
        ----------
        text : str
            The text to classify

        Returns
        -------
        dict
            {category:probability, category:probability...} or {} if no words
            matching any categories in the model were found

        """

        model = self.model

        tokens = gptc.tokenizer.tokenize(
            text, self.max_ngram_length, self.has_emoji
        )
        numbered_probs: Dict[int, float] = {}
        for word in tokens:
            try:
                weighted_numbers = gptc.weighting.weight(
                    [i / 65535 for i in cast(List[float], model[word])]
                )
                for category, value in enumerate(weighted_numbers):
                    try:
                        numbered_probs[category] += value
                    except KeyError:
                        numbered_probs[category] = value
            except KeyError:
                pass
        total = sum(numbered_probs.values())
        probs: Dict[str, float] = {
            cast(List[str], model["__names__"])[category]: value / total
            for category, value in numbered_probs.items()
        }
        return probs

    def classify(self, text: str) -> Union[str, None]:
        """Classify text.

        Parameters
        ----------
        text : str
            The text to classify

        Returns
        -------
        str or None
            The most likely category, or None if no words matching any
            category in the model were found.

        """
        probs: Dict[str, float] = self.confidence(text)
        try:
            return sorted(probs.items(), key=lambda x: x[1])[-1][0]
        except IndexError:
            return None
