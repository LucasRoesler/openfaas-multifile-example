
import unicodedata
import os
from typing import DefaultDict, Dict, List

from operator import itemgetter
from collections import defaultdict

FILE = os.path.dirname(__file__)
STOPWORDS = set(
    map(str.lower,
        map(str.strip,
            open(os.path.join(FILE, 'stopwords'), 'r').readlines()
            )
        )
)


def process_text(text: bytes) -> Dict[str, int]:
    """Splits a long text into words a count of interesting words in the text.

    process_text will elimate any of the stopwords, punctuation, and normalize
    the text to merge cases and plurals into a single value.
    """
    words = text.decode("utf-8").split()
    # remove stopwords
    # remove 's
    words = [
        word[:-2] if word.lower().endswith(("'s",))
        else word
        for word in words
    ]
    # remove numbers
    words = [word for word in words if not word.isdigit()]
    words = [strip_punctuation(word) for word in words]
    words = [word for word in words if word.lower() not in STOPWORDS]

    return process_tokens(words)


def process_tokens(words: List[str]) -> Dict[str, int]:
    """Normalize cases and remove plurals.
    """
    # d is a dict of dicts.
    # Keys of d are word.lower(). Values are dicts
    # counting frequency of each capitalization
    d: DefaultDict = defaultdict(dict)
    for word in words:
        word_lower = word.lower()
        # get dict of cases for word_lower
        case_dict = d[word_lower]
        # increase this case
        case_dict[word] = case_dict.get(word, 0) + 1
    # merge plurals into the singular count (simple cases only)
    merged_plurals = {}
    for key in list(d.keys()):
        if key.endswith('s') and not key.endswith("ss"):
            key_singular = key[:-1]
            if key_singular in d:
                dict_plural = d[key]
                dict_singular = d[key_singular]
                for word, count in dict_plural.items():
                    singular = word[:-1]
                    dict_singular[singular] = (
                        dict_singular.get(singular, 0) + count)
                merged_plurals[key] = key_singular
                del d[key]
    fused_cases = {}
    item1 = itemgetter(1)
    for word_lower, case_dict in d.items():
        # Get the most popular case.
        first = max(case_dict.items(), key=item1)[0]
        fused_cases[first] = sum(case_dict.values())
    return fused_cases


def strip_punctuation(text: str) -> str:
    punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
    return ''.join(x for x in text
                   if unicodedata.category(x) not in punctutation_cats)
