import logging
from typing import List, Set

import numpy as np
import unidecode
from dataproc.words.corpus import Corpus
from dataproc.words.parsers import doc_parser
from gensim import models
from gensim.corpora.dictionary import Dictionary
from gensim.models.word2vec import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# LEGACY module
# maybe using for trainning new word2vec models

logger = logging.getLogger(__name__)


class W2VModel:
    """ This is a wrapper of the gensim.Word2Vec model 
    For now the intention of this class is only for training new models.
    """

    def __init__(self, model: Word2Vec, stopw: List[str],
                 lang="es", strip_accents=True):
        #self.vs = vector_size
        #self.w = workers
        self.strip = strip_accents
        self.model: Word2Vec = model
        self.stopw: List[str] = stopw
        self.lang = lang
        self.vector_size = model.vector_size

    def doc_parser(self, text) -> List[str]:
        return doc_parser(text, self.stopw, strip_accents=self.strip)

    def get_vector2(self, sentences: List[str]):
        """
        From a list of words it gets a vector for a document.
        """
        vectors = []
        for word in sentences:
            try:
                _vect = self.model.wv[word]
                vectors.append(_vect)
            except KeyError:
                pass

        if len(vectors) > 0:
            return np.sum(np.array(vectors), axis=0) / (len(vectors) + 0.001)
        else:
            return np.zeros((self.vector_size,))

    @classmethod
    def fit(cls, df, stopw, column="text",
            strip_accents=True,
            lang="es",
            vector_size=100, workers=4):
        corpus = Corpus(df,
                        stopw=stopw,
                        column=column,
                        strip_accents=strip_accents)
        model = Word2Vec(sentences=corpus,
                         vector_size=vector_size,
                         workers=workers)
        obj = cls(model=model, stopw=stopw, lang=lang,
                  strip_accents=strip_accents)
        return obj

    def transform(self, text):
        parsed = self.doc_parser(text)
        return self.model.infer_vector(parsed)

    def most_similar(self, words, topn=5):
        return self.model.modest_similar(positive=words, topn=topn)

    def doesnt_match(self, words):
        """ Which of the below does not belong in the sequence?
        """
        return self.model.doesnt_match(words)

    def similarity(self, text1, text2):
        vec1 = self.get_vector2(self.doc_parser(text1))
        vec2 = self.get_vector2(self.doc_parser(text2))
        simil = cosine_similarity([vec1], [vec2])
        return simil[0][0]

    def save(self, filepath):
        # options = dict(lang=self.lang,
        #               vector_size=self.vector_size,
        #               strip=self.strip,
        #               )
        self.model.save(f"{filepath}.model")

        # joptions = json.dumps(options)
        # with open(f"{filepath}.json", "w") as f:
        #    f.write(joptions)

    @classmethod
    def load_model(cls, filepath, stopw,
                   lang="es", vector_size=100, strip=True):
        wv = Word2Vec.load(filepath)
        # with open(f"{filepath}.json", "r") as f:
        #   data = f.read()
        # options = json.loads(data)
        # stopw = load_stop(stop_path, lang=options["lang"])

        return cls(wv, stopw,
                   lang=lang,
                   vector_size=vector_size,
                   strip_accents=strip)


class LDAModel:

    def __init__(self, lang, column, num_topics=8, workers=4):
        # self.lang = lang
        self.column = column
        self.stopw = load_stop(lang=lang)
        self.dict_ = None
        self.model = None
        self._topics = num_topics
        self._workers = workers

    def fit(self, df):
        sentences = Corpus(df, stopw=self.stopw, column=self.column)
        self.dict_ = Dictionary(sentences)
        corpus = [self.dict_.doc2bow(text)
                  for text in Corpus(df,
                                     stopw=self.stopw,
                                     column=self.column)]

        self.model = models.ldamulticore.LdaMulticore(corpus,
                                                      id2word=self.dict_,
                                                      num_topics=self._topics,
                                                      workers=self._workers)

    def predict(self, text):
        tokens = doc_parser(text, self.stopw, strip_accents=True)
        vec = self.dict_.doc2bow(tokens)
        calc = self.model[vec]
        calc.sort(key=lambda tup: tup[1], reverse=True)
        return calc

    def save(self, filepath):
        pass

    def show_topics(self):
        return self.model.show_topics()

    @classmethod
    def load(cls, lang, column, base_path):
        model = cls(lang=lang, column=column)
        _dict = Dictionary.load(f"{base_path}.dict")
        _lda = models.LdaModel.load(f"{base_path}.model")
        model.dict_ = _dict
        model.model = _lda
        return model
