from collections import Counter
from typing import List

from dataproc.news.ml_models import SectionML
from dataproc.words.entities import Entities
from dataproc.words.models import W2VModel
from dataproc.words.utils import extract_entities


def twitter_entity(labels):
    final_label = []
    for word in labels:
        new_word = []
        for w in word.split():
            if w != "RT":
                new_word.append(w)
        if new_word:
            final_label.append(" ".join(new_word))
    return final_label


class TweetML:

    def __init__(self, nlp, stopw: List[str], wv: W2VModel,
                 section_ml: SectionML, lang: str):
        self.nlp = nlp
        self.stopw = stopw
        self.wv = wv
        self.section_ml = section_ml
        self.lang = lang

    def predict_section(self, sentences: List[str], barrier=0.3):
        return self.section_ml.predict_list(sentences, barrier=barrier)

    def get_entities(self, text: str):
        doc = self.nlp(text)
        _, labels = extract_entities(doc)
        final_labels = {}

        for ent in ["ORG", "LOC", "PER"]:
            if labels.get(ent):
                final_labels[ent] = twitter_entity(labels[ent])
        # final_entities
        entities = {}
        # print(final_labels)
        for x in ["ORG", "LOC", "PER"]:
            if final_labels.get(x):
                e = Entities.most_common(final_labels[x], text)
                entities[x] = [e[0] for e in e.counter.most_common()[:2]]
        # print(f"{x}: ", pers.counter.most_common()[:2])
    # pers = Persons.most_common(final_labels["PER"], text)
    # entities["PER"] = [p[0] for p in pers.counter.most_common()[:2]]
        return entities
