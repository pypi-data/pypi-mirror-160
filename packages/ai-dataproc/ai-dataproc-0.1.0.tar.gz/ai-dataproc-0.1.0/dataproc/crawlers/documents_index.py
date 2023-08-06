from typing import List

import cloudpickle
import marisa_trie
import requests
from dataproc.conf import Config


class DocumentsIndex:
    """ This a hand crafted index to check if previous urls was crawled. 
    It will save the data in the nginx fileserver. 

    """

    FILENAME = "docs_index.pickle"

    def __init__(self, remote_path: str, fileserver=Config.FILESERVER):
        self.index_url = f"{fileserver}/{remote_path}/{self.FILENAME}"
        self.index = self._load()
        #self.is_new = False
        # if not self.index:
        #    self.index = marisa_trie.Trie(new_list)
        #    self.is_new = True

    def _load(self):
        data = requests.get(self.index_url)
        if data.status_code == 200:
            docs_index = cloudpickle.loads(data.content)
            return docs_index

    def valid_docs(self, new_list: List[str]):
        if self.index:
            valid_docs = []
            for x in new_list:
                if x not in self.index:
                    valid_docs.append(x)
        else:
            valid_docs = new_list.copy()
            self.index = marisa_trie.Trie(valid_docs)
        return valid_docs

    def update(self, valid_links: List[str]):
        old = self.index.keys()
        for x in valid_links:
            if x not in self.index:
                old.append(x)
        self.index = marisa_trie.Trie(old)
        index_bytes = cloudpickle.dumps(self.index)
        r = requests.put(self.index_url, data=index_bytes)
        return r

    def delete(self):
        requests.delete(self.index_url)
