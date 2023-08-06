# SPDX-License-Identifier: LGPL-3.0-or-later

"""General-Purpose Text Classifier"""

from gptc.compiler import compile as compile
from gptc.classifier import Classifier as Classifier
from gptc.pack import pack as pack
from gptc.tokenizer import has_emoji as has_emoji
from gptc.model_info import model_has_emoji as model_has_emoji
from gptc.exceptions import (
    GPTCError as GPTCError,
    ModelError as ModelError,
    UnsupportedModelError as UnsupportedModelError,
)
