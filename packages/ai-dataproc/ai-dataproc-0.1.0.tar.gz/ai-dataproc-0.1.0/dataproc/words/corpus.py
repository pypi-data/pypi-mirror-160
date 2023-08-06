import multiprocessing as mp
from typing import List, Any

import numpy as np
from dataproc.conf import Config
from dataproc.words.utils import locale, norm_l2_np


class CorpusVectorizer:
    # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """ It uses word2vec model to parse texts and get the vectors of this. """

    def __init__(self, locale_: str,
                 base_path=Config.BASE_PATH,
                 with_nlp=False, nlp_rank=False, l2_norm=False, mp_process=True):

        # pylint: disable=too-many-arguments
        self.locale_opts = locale[locale_]
        self.with_nlp = with_nlp
        self.nlp_rank = nlp_rank
        self.l2_norm = l2_norm
        self.mp_process = mp_process
        self.X: List[str] = []
        self._vectors: Any = None
        self._base_path = base_path

    @staticmethod
    def get_locales():
        return locale.keys()

    def _process(self, return_list):
        # pylint: disable=import-outside-toplevel
        from dataproc.words.ml_models import create_word_actor
        words = create_word_actor(
            self._base_path, self.locale_opts, with_nlp=self.with_nlp, nlp_rank=self.nlp_rank)

        for doc in self.X:
            _parsed = words.doc_parser(doc)
            if self.l2_norm:
                v = norm_l2_np(words.get_vector2(_parsed))
            else:
                v = words.get_vector2(_parsed)
            return_list.append(v)

    def fit_transform(self, X: List[str]):
        self.X = X
        return_list: List[str] = []
        if self.mp_process:
            manager = mp.Manager()
            return_list = manager.list()
            proc = mp.Process(target=self._process, args=(return_list,))
            proc.start()
            proc.join()
            return np.asarray(list(return_list))

        self._process(return_list)
        self._vectors = np.asarray(return_list)
        return self._vectors
