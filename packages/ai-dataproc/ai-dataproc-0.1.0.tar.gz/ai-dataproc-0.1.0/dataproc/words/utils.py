import re
import sqlite3
from dataclasses import dataclass
from typing import Any, Dict

import numpy as np
from dataproc.words.iso_639 import find_lang_name
from iso3166 import countries
from langcodes import Language, standardize_tag

# https://unicode-org.github.io/icu/userguide/locale/
# LANG code is ISO-639: "es", "en"...
# COUNTRY is ISO-3166
locale = {
    "es-AR":  dict(
        spacy="spacy/es_core_news_md-3.1.0",
        spacy_en="spacy/en_core_web_sm-3.1.0",
        section_model="section_classifier.ar.20211013",
        # wv_model="news_ar_word2vec.kv",
        wv_model="word2vec/es/word2vec.uncased.wordvectors",
        phrases="phrases_frozen.uncased.pkl",
        wv_model_cased="word2vec/es/word2vec.cased.wordvectors",
        phrases_cased="phrases_frozen.cased.pkl",
        lang="es",
        country="AR",
        locale="es-AR",
        translate_romance_en="Helsinki-NLP/opus-mt-ROMANCE-en",
        translate_en_romance="Helsinki-NLP/opus-mt-en-ROMANCE",
        nli_model_en="cross-encoder/nli-distilroberta-base",
        labse="setu4993/smaller-LaBSE",
    ),
    "es":  dict(spacy="spacy/es_core_news_md-3.1.0",
                section_model=None,
                # wv_model="SBW-vectors-300-min5_es.keys",
                wv_model="word2vec/es/word2vec.uncased.wordvectors",
                phrases="phrases_frozen.uncased.pkl",
                wv_model_cased="word2vec/es/word2vec.cased.wordvectors",
                phrases_cased="phrases_frozen.cased.pkl",
                lang="es",
                country=None,
                locale="es",
                ),
    "en-US":  dict(spacy="spacy/en_core_web_sm-3.1.0",
                   section_model=None,
                   wv_model="glove-wiki-gigaword-200",
                   lang="en",
                   country="US",
                   locale="en-US",
                   nli_model_en="cross-encoder/nli-distilroberta-base",
                   ),
    "en":  dict(spacy="spacy/en_core_web_sm-3.1.0",
                section_model=None,
                # wv_model="glove-wiki-gigaword-200",
                wv_model="word2vec/es/word2vec.uncased.wordvectors",
                phrases="phrases_frozen.uncased.pkl",
                wv_model_cased="word2vec/es/word2vec.cased.wordvectors",
                phrases_cased="phrases_frozen.cased.pkl",
                lang="en",
                country=None,
                locale="en",
                nli_model_en="cross-encoder/nli-distilroberta-base",
                ),
    "pt":  dict(spacy="spacy/pt_core_news_md-3.1.0",
                section_model=None,
                wv_model="pt_word2vec.model",
                lang="es",
                country="BR",
                locale="pt-BR",
                ),
    "pt-BR":  dict(spacy="spacy/pt_core_news_md-3.1.0",
                   section_model=None,
                   wv_model="pt_word2vec.model",
                   lang="es",
                   country="BR",
                   locale="pt-BR",
                   ),
    "es-CL":  dict(spacy="spacy/es_core_news_md-3.1.0",
                   section_model=None,
                   wv_model="news_ar_word2vec.model",
                   lang="es",
                   country="CL",
                   locale="es-CL",
                   )
}


@dataclass
class Entity:
    txt: str
    start_char: int
    end_char: int
    label: str


def extract_entities(doc):
    """ Gets a spacy doc object """
    _entities = []
    by_label = {}
    for ent in doc.ents:
        e = Entity(ent.text, ent.start_char, ent.end_char, ent.label_)
        _entities.append(e)
        # Ordering by label
        if by_label.get(e.label):
            by_label[e.label].append(e.txt)
        else:
            by_label.update({e.label: [e.txt]})

    return _entities, by_label


def get_locale(loc: str) -> Dict[str, Any]:
    return locale[loc]


def get_lang(lang):
    """ simple wrapper """
    return find_lang_name(lang)


def get_country(country):
    """ simple wrapper """
    return countries.get(country)


def build_locale(lang, country):
    """ It builds a locale based on ICU which is a combination
    of ISO-639 (lang) and ISO-3166 (countries)
    https://unicode-org.github.io/icu/userguide/locale/
    """
    c = countries.get(country.lower())
    _lang = find_lang_name(lang)[0][0]
    code = f"{_lang}_{c.alpha2}"
    return standardize_tag(code)


def reverse_locale(loc, lang_code=True, country_code=True):
    l = Language.get(loc)
    if lang_code:
        _lang = l.language
    else:
        _lang = l.language_name()
    if country_code:
        country = l.territory
    else:
        country = l.territory_name()
    return _lang, country


def generate_ngrams(s, n):
    # Convert to lowercases
    s = s.lower()

    # Replace all none alphanumeric characters with spaces
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

    # Break sentence in the token, remove empty tokens
    tokens = [_token for _token in s.split(" ") if _token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def norm_l2_np(vect):
    # same function as pytorch
    return vect / np.linalg.norm(vect)


class WordSearch:
    """Based  on a list we want to get uniques names ready to be used
    with fts5 type data from sqlite3 which allow us to perform fuzzy 
    search over a set of data."""

    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self._create_tables()

    @staticmethod
    def _run_query(cursor: sqlite3.Cursor, q: str):
        """ sqlite helper to run queries.
        """
        return cursor.execute(q).fetchall()

    def _create_tables(self):
        cur = self.db.cursor()
        cur.execute(
            'create virtual table vtags using fts5(name, tokenize="ascii");')
        # cur.execute(
        #    'create virtual table bigram using fts5(first, second, tokenize="ascii");')

        # cur.execute(
        #    'create virtual table finalnames using fts5(fullname, tokenize="ascii");')
        # This second table is used as a index to avoid repeated names
        # cur.execute("""CREATE TABLE tags
        # (id INTEGER PRIMARY KEY,tag TEXT NOT NULL UNIQUE);""")

        cur.close()

    def add(self, name):
        cur = self.db.cursor()
        try:
            cur.execute("insert into vtags (name) values (?);", (name,))
            self.db.commit()
        except sqlite3.IntegrityError:
            pass
        except sqlite3.OperationalError:
            pass

        cur.close()

    def add_batch(self, names):
        cur = self.db.cursor()
        for n in names:
            cur.execute("insert into vtags(name) values(?);", (n,))

        self.db.commit()
        cur.close()

    def get(self, name, limit=1):
        cur = self.db.cursor()
        try:
            result = self._run_query(cur, f"""select *
                                    from vtags
                                    where name MATCH '"{name}" *'
                                    limit {limit}""")
        except sqlite3.OperationalError:
            result = []
        cur.close()
        return [r for r, in result]
