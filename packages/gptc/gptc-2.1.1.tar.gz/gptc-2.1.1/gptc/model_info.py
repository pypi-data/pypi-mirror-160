# SPDX-License-Identifier: LGPL-3.0-or-later

import gptc.compiler
from typing import Dict, Union, cast, List


def model_has_emoji(model: gptc.compiler.MODEL) -> bool:
    return cast(int, model.get("__emoji__", 0)) == 1
