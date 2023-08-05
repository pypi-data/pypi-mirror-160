# GPTC

General-purpose text classifier in Python

GPTC provides both a CLI tool and a Python library.

## Installation

    pip install gptc[emoji] # handles emojis! (see section "Emoji")
    # Or, if you don't need emoji support,
    pip install gptc # no dependencies!

## CLI Tool

### Classifying text

    gptc classify [-n <max_ngram_length>] <compiled model file>

This will prompt for a string and classify it, then print (in JSON) a dict of
the format `{category: probability, category:probability, ...}` to stdout. (For
information about `-n <max_ngram_length>`, see section "Ngrams.")

Alternatively, if you only need the most likely category, you can use this:

    gptc classify [-n <max_ngram_length>] <-c|--category> <compiled model file>

This will prompt for a string and classify it, outputting the category on
stdout (or "None" if it cannot determine anything).

### Compiling models

    gptc compile [-n <max_ngram_length>] <raw model file>

This will print the compiled model in JSON to stdout.

### Packing models

    gptc pack <dir>

This will print the raw model in JSON to stdout. See `models/unpacked/` for an
example of the format. Any exceptions will be printed to stderr.

## Library

### `gptc.Classifier(model, max_ngram_length=1)`

Create a `Classifier` object using the given *compiled* model (as a dict, not
JSON).

For information about `max_ngram_length`, see section "Ngrams."

#### `Classifier.confidence(text)`

Classify `text`. Returns a dict of the format `{category: probability,
category:probability, ...}`

#### `Classifier.classify(text)`

Classify `text`. Returns the category into which the text is placed (as a
string), or `None` when it cannot classify the text.

#### `Classifier.model`

The classifier's model.

#### `Classifier.has_emoji`

Check whether emojis are supported by the `Classifier`. (See section "Emoji.")
Equivalent to `gptc.has_emoji and gptc.model_has_emoji(model)`.

### `gptc.compile(raw_model, max_ngram_length=1)`

Compile a raw model (as a list, not JSON) and return the compiled model (as a
dict).

For information about `max_ngram_length`, see section "Ngrams."

### `gptc.pack(directory, print_exceptions=False)

Pack the model in `directory` and return a tuple of the format:

    (raw_model, [(exception,),(exception,)...])

Note that the exceptions are contained in single-item tuples. This is to allow
more information to be provided without breaking the API in future versions of
GPTC.

See `models/unpacked/` for an example of the format.

### `gptc.has_emoji`

`True` if the `emoji` package is installed (see section "Emoji"), `False`
otherwise.

### `gptc.model_has_emoji(compiled_model)`

Returns `True` if `compiled_model` was compiled with emoji support, `False`
otherwise.

## Ngrams

GPTC optionally supports using ngrams to improve classification accuracy. They
are disabled by default (maximum length set to 1) for performance and
compatibility reasons. Enabling them significantly increases the time required
both for compilation and classification. The effect seems more significant for
compilation than for classification. Compiled models are also much larger when
ngrams are enabled. Larger maximum ngram lengths will result in slower
performance and larger files. It is a good idea to experiment with different
values and use the highest one at which GPTC is fast enough and models are
small enough for your needs.

Once a model is compiled at a certain maximum ngram length, it cannot be used
for classification with a higher value. If you instantiate a `Classifier` with
a model compiled with a lower `max_ngram_length`, the value will be silently
reduced to the one used when compiling the model.

Models compiled with older versions of GPTC which did not support ngrams are
handled the same way as models compiled with `max_ngram_length=1`.

## Emoji

If the [`emoji`](https://pypi.org/project/emoji/) package is installed, GPTC
will automatically handle emojis the same way as words. If it is not installed,
GPTC will still work but will ignore emojis.

`emoji` must be installed on both the system used to compile the model and the
system used to classify text. Emojis are ignored if it is missing on either
system.

## Model format

This section explains the raw model format, which is how you should create and
edit models.

Raw models are formatted as a list of dicts. See below for the format:

    [
        {
            "text": "<text in the category>",
            "category": "<the category>"
        }
    ]

GPTC handles models as Python `list`s of `dict`s of `str`s (for raw models) or
`dict`s of `str`s and `float`s (for compiled models), and they can be stored
in any way these Python objects can be. However, it is recommended to store
them in JSON format for compatibility with the command-line tool.

## Example model

An example model, which is designed to distinguish between texts written by
Mark Twain and those written by William Shakespeare, is available in `models`.
The raw model is in `models/raw.json`; the compiled model is in
`models/compiled.json`.

The example model was compiled with `max_ngram_length=10`.

## Benchmark

A benchmark script is available for comparing performance of GPTC between
different Python versions. To use it, run `benchmark.py` with all of the Python
installations you want to test. It tests both compilation and classification.
It uses the default Twain/Shakespeare model for both, and for classification it
uses [Mark Antony's "Friends, Romans, countrymen"
speech](https://en.wikipedia.org/wiki/Friends,_Romans,_countrymen,_lend_me_your_ears)
from Shakespeare's *Julius Caesar*.
