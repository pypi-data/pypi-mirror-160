from collections import Counter
from typing import List

import unidecode
from dataproc.words.utils import WordSearch, extract_entities


class Keywords:
    """ Extracts keywords from a test using textrank and Spacy NER """

    def __init__(self, stopw: List[str]):
        self.stopw = stopw

    def get_keys(self, doc, top_n=3):
        keys = []
        for phrase in doc._.phrases[:top_n]:
            keys.append(self.remove_stop(phrase.text))
        return keys

    def remove_stop(self, word):
        _new = []

        for x in word.split():
            transformed = unidecode.unidecode(x.lower().strip())
            if transformed not in self.stopw:
                _new.append(x)
        return " ".join(_new).strip()

    def remove_stop_from_phrase(self, phrase):
        _new = []
        for w in phrase:
            # tokens = doc_parser(w, self.stopw, strip_accents=True)
            removed = self.remove_stop(w)
            # removed = " ".join(tokens)
            if removed and not len(removed.split()) > 3:
                _new.append(removed)
        return _new

    def flat_entities(self, ents, include_misc=True):
        all_ = []
        for lbl in ents:
            _new = self.remove_stop_from_phrase(ents[lbl])
            if not include_misc:
                if lbl != "MISC" and _new:
                    all_.extend(_new)
            else:
                all_.extend(_new)
        return all_

    def extract(self, doc, misc=True, keys_top=5, keys_weight=3):
        _, lbls = extract_entities(doc)

        all_ = self.flat_entities(lbls, include_misc=misc)
        keys_ = self.get_keys(doc, top_n=keys_top)
        keys_ = list(filter(lambda x: len(x.split()) < 3, keys_))
        all_.extend(keys_ * keys_weight)
        c = Counter()
        ws = WordSearch()
        ws.add_batch(all_)
        for w in all_:
            res = ws.get(w)
            if res:
                c.update(res)
        return c
