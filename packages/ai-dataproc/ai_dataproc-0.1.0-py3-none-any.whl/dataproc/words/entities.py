import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from typing import List


@dataclass
class EntityData:
    entities: List[str]
    counter: Counter
    # tokens: List[str]


def _run_query(cursor: sqlite3.Cursor, q: str):
    """ sqlite helper to run queries.
    """
    return cursor.execute(q).fetchall()


def _longest(data):
    """
    Helper, this choose the fullname with more words:
    [('Cristina Kirchner',), ('Cristina Fernández de Kirchner',), ('Cristina',)]
    """
    aux = 0
    final = None
    for x in data:
        if len(x[0].split()) > aux:
            final = x
            aux = len(x)
    return final

def _shortest(data):
    """
    Helper, this choose the phrase with less words:
    [('Cristina Kirchner',), ('Cristina Fernández de Kirchner',), ('Cristina',)]
    """
    aux = 0
    final = None
    for x in data:
        if len(x[0].split()) > aux:
            final = x
            aux = len(x)
    return final




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


class Entities:
    """Based  on a list we want to get uniques names ready to be used
    with fts5 type data from sqlite3 which allow us to perform fuzzy 
    search over a set of data."""

    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self._create_tables()

    @classmethod
    def most_common(cls, words: List[str], text: str) -> EntityData:
        """
        We need to find how many times each person is mentioned in the text.
        For that purpose, we calculate ngrams of size 2 for the text and perform
        a fuzzy search for each ngram.

        A possible improvement could be to cutoff stop and not common words,
        or compare against "PER" dataset.
        """
        entities = cls()
        uniques = entities.get_unique(words)
        c = entities.ngram_search(text)
        ps = [u[0] for u in uniques]

        return EntityData(entities=ps, counter=c)

    def _create_tables(self):
        cur = self.db.cursor()
        cur.execute(
            'create virtual table names using fts5(fullname, tokenize="ascii");')
        cur.execute(
            'create virtual table finalnames using fts5(fullname, tokenize="ascii");')
        # This second table is used as a index to avoid repeated names
        cur.execute("""CREATE TABLE normal
        (id INTEGER PRIMARY KEY,fullname TEXT NOT NULL UNIQUE);""")

        cur.close()

    def get_unique(self, persons: List[str]):
        """
        Based on a list of names it identify who is unique. 
        It prioritizes longs names over shorts.
        """
        cur = self.db.cursor()
        for x in persons:
            # if len(x.split()) > 1:
            try:
                cur.execute(
                    "insert into normal (fullname) values (?);", (x,))
                cur.execute(
                    'insert into names (fullname) values (?);', (x,))
            except sqlite3.IntegrityError:
                pass

        self.db.commit()

        all_names = _run_query(cur, "select * from names;")
        unique_names = set()
        for n in all_names:
            word = n[0]
            word = word.replace("'", " ")

            try:
                query = f"""select * from names where fullname match '"{word}" *' limit 5"""
                result = cur.execute(query).fetchall()

                if len(result) > 1:
                    _rsp = _shortest(result)
                    unique_names.add(_rsp[0])
                else:
                    unique_names.add(result[0][0])
            except sqlite3.OperationalError as e:
                raise(e)
            # except IndexError as e:
            #    breakpoint()

        for x in unique_names:
            cur.execute('insert into finalnames (fullname) values (?);', (x,))

        self.db.commit()
        rows = _run_query(cur, "select * from finalnames;")

        cur.close()
        return rows

    def fuzzy_search(self, name):
        cur = self.db.cursor()
        result = _run_query(cur, f"""select *
                                    from finalnames
                                    where fullname MATCH '"{name}" *'
                                    limit 1""")
        cur.close()
        return result

    def ngram_search(self, text) -> Counter:
        """ Based on the names previously loaded with `get_uniques`
        this method receive a text and counts how often each name appears
        """
        cur = self.db.cursor()
        c = Counter()
        for x in generate_ngrams(text, 2):
            result = _run_query(cur, f"""select *
                                        from finalnames
                                        where fullname MATCH '"{x}" *'
                                        limit 1""")
            if len(result) > 0:
                c.update(result[0])

        return c
