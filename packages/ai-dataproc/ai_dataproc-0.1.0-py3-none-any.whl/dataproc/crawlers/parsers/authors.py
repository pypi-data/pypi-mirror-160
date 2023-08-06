from dataclasses import dataclass
from typing import Any, Dict, List, Set, Union

import unidecode
from dataproc.words.parsers import doc_parser


@dataclass
class AuthorData:
    authors: Union[List[str], None]
    authors_norm: Union[List[str], None]


class Authors:

    def __init__(self, stopwords: Set[str]):
        self.stopw = stopwords

    def normalize_authors_df(self, row):
        """It gets a row from a dataframe"""

        _authors = []
        if isinstance(row.authors, dict):
            # print([authors.get("name")])
            a = row.authors.get("name")
            if a:
                parsed = doc_parser(a, stop_words=self.stopw)
                _authors.append(".".join(parsed))
        elif isinstance(row.authors, list):
            for author in row.authors:
                if isinstance(author, dict):
                    a = author.get("name")
                    if a:
                        parsed = doc_parser(a, stop_words=self.stopw)
                        _authors.append(".".join(parsed))
                else:
                    parsed = doc_parser(author, stop_words=self.stopw)
                    _authors.append(".".join(parsed))

        if not _authors:
            return None
        return _authors

    def normalize_authors(self, authors: Union[List[Any], Dict[str, Any]]) \
            -> Union[List[str], None]:
        """ It gets an author object from ld_data and normalized it 
        as removing stop words, undercasing all and replacing spaces by dots."""

        _authors = []
        if isinstance(authors, dict):
            # print([authors.get("name")])
            a = authors.get("name")
            if a:
                # parsed = news_actor.words.doc_parser(a)
                _authors.append(a)
        elif isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict):
                    a = author.get("name")
                    if a:
                        _authors.append(a)
                else:
                    parsed = doc_parser(author, stop_words=self.stopw)
                    _authors.append(".".join(parsed))

        if not _authors:
            return None
        return _authors


def _remove_stop(word, stopw):
    _new = []

    for x in word.split():
        transformed = unidecode.unidecode(x.lower().strip())
        if transformed not in stopw:
            _new.append(transformed)
    return _new


def _extract_from_ld(ld_data) -> Union[List[str], Dict[str, str], None]:
    authors = None
    if isinstance(ld_data, list):
        for d in ld_data:
            if "author" in d.keys():
                authors = d["author"]
                break
    elif isinstance(ld_data, dict):
        authors = ld_data.get("author")
    return authors


def get_from_ld(ld_data, stopw: List[str]) -> AuthorData:
    """ Get and normalized authors extracted from LD_DATA """

    authors = _extract_from_ld(ld_data)
    _authors_norm = []
    _authors = []
    # import pdb; pdb.set_trace()
    if isinstance(authors, dict):
        # print([authors.get("name")])
        a = authors.get("name")
        if a:
            # parsed = news_actor.words.doc_parser(a)
            parsed = _remove_stop(a, stopw)
            _authors_norm.append(".".join(parsed))
            _authors.append(a)
    elif isinstance(authors, list):
        for author in authors:
            if isinstance(author, dict):
                a = author.get("name")
                if a:
                    parsed = _remove_stop(a, stopw)
                    _authors_norm.append(".".join(parsed))
                    _authors.append(a)

            else:
                parsed = _remove_stop(author, stopw)
                _authors_norm.append(".".join(parsed))
                _authors.append(author)

    if not _authors:
        return None
    return AuthorData(authors=_authors, authors_norm=_authors_norm)
