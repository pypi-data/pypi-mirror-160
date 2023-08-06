"""Classify nouns as concrete nouns (1) and none-concrete nouns (0).

Based on https://stackoverflow.com/questions/28575082/classify-a-noun-into-abstract-or-concrete-using-nltk-or-similar.
"""
# pylint: disable=invalid-name
from typing import List

import numpy as np
import spacy
from logzero import logger
from sklearn.linear_model import LogisticRegression

try:
    nlp = spacy.load("en_core_web_md")  # !python -m spacy download en_core_web_md
except Exception:
    try:
        spacy.cli.download("en_core_web_md")
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        nlp = spacy.load("en_core_web_md")
    except Exception as exc:
        logger.error(exc)
        raise

classes = ['concrete-noun', 'not-concrete-noun']
# todo: add more examples
train_set = [
    [
        "apple",
        "owl",
        "house",
        "houses",
        "owls",
        "apples",
        "rivers",
        "river",
        "chair",
        "chairs",
        "book",
        "books",
    ],
    [
        "agony",
        "knowledge",
        "process",
        "juice",
        "my",
        "do",
        "make",
        "love",
        "thought",
        "Xingjian",
        "Tian",
        'comfort',
    ],
]

X = np.stack([list(nlp(w))[0].vector for part in train_set for w in part])
y = [label for label, part in enumerate(train_set) for _ in part]
classifier = LogisticRegression(C=0.1, class_weight="balanced").fit(X, y)


def conc_nouns(text: str) -> List[int]:
    """Classify concrte nouns (1).

    Args:
        text: a string
    Returns:
        a vector, 1: concrete nouns, 0: none-concrete nouns

    Additional: conc_nouns.words: list of tokens
    """
    try:
        text = str(text)
    except Exception as exc:
        logger.error(exc)
        raise

    words = nlp(text)

    conc_nouns.tokens = [str(tok) for tok in words]

    lst = []
    for token in words:
        if token.pos_ in ["NOUN"]:
            _ = classes[classifier.predict([token.vector])[0]]
            if _ in ["concrete-noun"]:
                lst.append(1)
            else:
                lst.append(0)
        else:
            lst.append(0)

    return lst
