# SPDX-License-Identifier: LGPL-3.0-or-later

import sys
import os
from typing import List, Dict, Tuple


def pack(
    directory: str, print_exceptions: bool = False
) -> Tuple[List[Dict[str, str]], List[Tuple[Exception]]]:
    paths = os.listdir(directory)
    texts: Dict[str, List[str]] = {}
    exceptions = []

    for path in paths:
        texts[path] = []
        try:
            for file in os.listdir(os.path.join(directory, path)):
                try:
                    with open(os.path.join(directory, path, file)) as f:
                        texts[path].append(f.read())
                except Exception as e:
                    exceptions.append((e,))
                    if print_exceptions:
                        print(e, file=sys.stderr)
        except Exception as e:
            exceptions.append((e,))
            if print_exceptions:
                print(e, file=sys.stderr)

    raw_model = []

    for category, cat_texts in texts.items():
        raw_model += [{"category": category, "text": i} for i in cat_texts]

    return raw_model, exceptions
