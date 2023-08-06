from typing import List

import numpy as np
# import spacy
from dataproc.words.entities import Entities
from dataproc.words.keywords import Keywords
from dataproc.words.parsers import doc_parser, load_stop
from dataproc.words.utils import extract_entities
from gensim.models import KeyedVectors, Word2Vec
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sknetwork.ranking import PageRank


def compute_similarity_m(vects):
    """get a cosine similarity matrix
    the diagonal where each element match with their self is
    matched to 0, if not pagerank fail
    """
    A = np.array(vects)
    # A_sparse = sparse.csr_matrix(A)
    M = cosine_similarity(A)

    for i in range(len(vects)):
        for j in range(len(vects)):
            if i == j:
                M[i][j] = 0.0
    return M


class WordActor:

    def __init__(self, stopw, wv_model: Word2Vec, nlp=None):
        self.nlp = nlp
        self.stopw = stopw
        self.wv: Word2Vec = wv_model
        self.vector_size = self.wv.vector_size
        self._keywords = Keywords(stopw)

    def load_nlp(self, nlp):
        self.nlp = nlp

    def doc_parser(self, txt, strip_accents=True):
        return doc_parser(txt, self.stopw, strip_accents=strip_accents)

    def get_vector2(self, s: List[str]):
        """ Get a vector from a list of texts
        if a sentence doesn't match, then it fills with zeros
        """
        vectors = []
        for word in s:
            try:
                _vect = self.wv[word]
                vectors.append(_vect)
            except KeyError:
                pass
        if len(vectors) > 0:
            return np.sum(np.array(vectors), axis=0) / (len(vectors) + 0.001)
        else:
            return np.zeros((self.vector_size,))

    def sentences(self, df, column="title", strip_accents=True):
        """
        Extracts words parsed and vectors from a corpus selected by column
        from a pandas DataFrame
        """

        sentences_vectors = []
        sentences = []
        for _, x in df[column].iteritems():
            s = doc_parser(x, self.stopw, strip_accents=strip_accents)
            v = self.get_vector2(s)
            sentences.append(s)
            sentences_vectors.append(v)
        return sentences_vectors, sentences

    def pagerank(self, df, column="title", strip_accents=True):
        """
        Estimate a pagerank by cosine_similarity
        """
        vects, _ = self.sentences(df, column, strip_accents)
        sim_M = compute_similarity_m(vects)
        adjacency = sparse.csr_matrix(sim_M)
        pagerank = PageRank()
        scores = pagerank.fit_transform(adjacency)
        return vects, scores

    def init_nlp_doc(self, text: str):
        return self.nlp(text)

    def get_entities(self, text: str):
        doc = self.init_nlp_doc(text)
        ents, labels = extract_entities(doc)
        return ents, labels

    def get_main_entities(self, text: str, top_n=2):
        doc = self.nlp(text)
        _, labels = extract_entities(doc)
        entities = {}
        for x in ["ORG", "LOC", "PER"]:
            try:
                ent = Entities.most_common(labels[x], text)
                entities[x] = ent.counter.most_common()[:top_n]
            except KeyError:
                pass
        return entities

    def keywords(self, text, common=3):
        doc = self.nlp(text)
        if common:
            keywords = self._keywords.extract(doc).most_common(common)
        else:
            keywords = self._keywords.extract(doc)
        return keywords

    def similarity(self, txt1, txt2, strip_accents=True):
        vec1 = self.get_vector2(doc_parser(txt1,
                                           self.stopw,
                                           strip_accents=strip_accents))
        vec2 = self.get_vector2(doc_parser(txt2, self.stopw,
                                           strip_accents=strip_accents))
        simil = cosine_similarity([vec1], [vec2])
        return simil[0][0]


def create_word_actor(base_path, opts, with_nlp=False, nlp_rank=False) -> WordActor:
    """ Helper function for a singleton word actor model """
    # pylint: disable=maybe-no-member
    # pylint: disable=
    nlp = None
    stopw = load_stop(base_path=f"{base_path}/models/",
                      lang=opts["lang"])
    wv_path = f"{base_path}/models/{opts['wv_model']}"
    wv = KeyedVectors.load(wv_path, mmap='r')

    if with_nlp:
        import spacy
        nlp = spacy.load(f"{base_path}/models/{opts['spacy']}")
        if nlp_rank:
            import pytextrank
            nlp.add_pipe("textrank")
    actor = WordActor(stopw, wv_model=wv, nlp=nlp)

    return actor
