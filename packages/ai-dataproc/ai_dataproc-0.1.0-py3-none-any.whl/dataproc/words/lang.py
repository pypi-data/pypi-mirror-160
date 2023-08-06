from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List

import langdetect


@dataclass
class PredictedCorpus:
    main: str
    main_proba: float
    counter: Counter
    langs: List[str]


def predict_txt(txt: str):
    """ predict lang of a string, if any returns None """
    try:
        p = langdetect.detect(txt)
    except langdetect.LangDetectException:
        p = None
    return p


def predict_corpus(texts: List[str]) -> PredictedCorpus:
    langs = [predict_txt(x) for x in texts]

    c: Counter = Counter(langs)
    commons = c.most_common(2)
    first_proba = commons[0][1] / len(texts)
    # second = commons[1][1] / len(texts)

    return PredictedCorpus(main=str(commons[0][0]), main_proba=first_proba, counter=c, langs=langs)
