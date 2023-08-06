from dataclasses import dataclass
from typing import List, Optional

from dataproc.words.parsers import doc_parser
from gensim import models
from gensim.corpora.dictionary import Dictionary
from nltk.stem import SnowballStemmer


@dataclass
class LsiModel:
    m: models.lsimodel.LsiModel
    dict_: Dictionary
    stopw: List[str]
    emoji: bool = True

    def get_topics(self, n: int):
        return self.m.print_topics(n)

    def get_vectorized(self, phrase: str):
        """ From a string, get vectors based on the
        trained model"""
        vec = self.dict_.doc2bow(
            doc_parser(phrase,
                       self.stopw,
                       emo_codes=self.emoji))
        return vec

    def predict(self, phrase):
        vec = self.get_vectorized(phrase)
        return self.m[vec]


@dataclass
class LsiTfidf:
    m: models.lsimodel.LsiModel
    dict_: Dictionary
    tfidf: models.tfidfmodel
    stopw: List[str]
    emoji: bool = True

    def get_topics(self, n: int):
        return self.m.print_topics(n)

    def get_vectorized(self, phrase: str):
        """ From a string, get vectors based on the
        trained model"""

        bow = self.dict_.doc2bow(
            doc_parser(phrase,
                       self.stopw, emo_codes=self.emoji))

        tfidf_corpus = self.tfidf[bow]
        return tfidf_corpus

    def predict(self, phrase):
        vec = self.get_vectorized(phrase)
        return self.m[vec]


def train_lsi_model(docs: List[str], topics: int,
                    stopw: List[str], emo_codes=True) -> LsiModel:
    """
    Train a lsi model but performs a tfidf transformation between
    """
    # stopw = load_stop(lang=lang)
    _corpus_generated = generate_corpus(docs, stopw=stopw, emo_codes=emo_codes)

    dict_ = Dictionary(_corpus_generated)

    corpus = [dict_.doc2bow(text)
              for text in generate_corpus(docs, stopw, emo_codes=emo_codes)]

    lsi = models.LsiModel(corpus, id2word=dict_, num_topics=2)

    return LsiModel(m=lsi, dict_=dict_, stopw=stopw, emoji=emo_codes)


def train_lsi_tfidf(docs: List[str], topics: int,
                    stopw: List[str],
                    emo_codes=True) -> LsiTfidf:
    """
    Train a lsi model
    """
    _corpus_generated = generate_corpus(docs, stopw=stopw, emo_codes=emo_codes)

    dict_ = Dictionary(_corpus_generated)

    corpus = [dict_.doc2bow(text)
              for text in generate_corpus(docs, stopw, emo_codes=emo_codes)]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    lsi_model = models.LsiModel(corpus_tfidf,
                                id2word=dict_,
                                num_topics=topics)

    return LsiTfidf(m=lsi_model,
                    dict_=dict_,
                    tfidf=tfidf,
                    stopw=stopw,
                    emoji=emo_codes)
