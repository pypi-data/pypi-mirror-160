# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataproc',
 'dataproc.clients',
 'dataproc.cmd',
 'dataproc.crawlers',
 'dataproc.crawlers.managers',
 'dataproc.crawlers.parsers',
 'dataproc.datasets',
 'dataproc.datasets.managers',
 'dataproc.datastore',
 'dataproc.hashes',
 'dataproc.regions',
 'dataproc.social',
 'dataproc.social.managers',
 'dataproc.social.twitter',
 'dataproc.words',
 'dataproc.words.transformers',
 'dataproc.zio']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.2,<2.0.0',
 'arrow>=1.2.0,<2.0.0',
 'cityhash>=0.2.3,<0.3.0',
 'cloudpickle>=2.0.0,<3.0.0',
 'cytoolz>=0.11.0,<0.12.0',
 'dateparser>=1.1.0,<2.0.0',
 'iso3166>=2.0.2,<3.0.0',
 'langdetect>=1.0.9,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'pytz>=2021.1,<2022.0',
 'xxhash>=2.0.2,<3.0.0']

extras_require = \
{':extra == "words"': ['transformers[torch]>=4.13.0,<5.0.0'],
 'crawl': ['pyarrow>=5.0.0,<6.0.0',
           'beautifulsoup4>=4.10.0,<5.0.0',
           'lxml>=4.6.3,<5.0.0',
           'ujson>=4.2.0,<5.0.0',
           'extruct>=0.13.0,<0.14.0',
           'feedparser>=6.0.8,<7.0.0',
           'reppy>=0.4.14,<0.5.0',
           'newspaper3k>=0.2.8,<0.3.0'],
 'social': ['tweepy>=4.0.0,<5.0.0',
            'pytrends>=4.7.3,<5.0.0',
            'pymediawiki>=0.7.1,<0.8.0'],
 'words': ['emoji>=1.5.0,<2.0.0',
           'gensim>=4.1.2,<5.0.0',
           'nltk>=3.6.4,<4.0.0',
           'scikit-learn>=1.0,<2.0',
           'spacy>=3.1.3,<4.0.0',
           'pytextrank>=3.2.1,<4.0.0',
           'scikit-network>=0.24.0,<0.25.0',
           'langcodes[data]>=3.2.1,<4.0.0',
           'tokenizers>=0.10.3,<0.11.0',
           'sentencepiece>=0.1.96,<0.2.0',
           'sentence-transformers>=2.1.0,<3.0.0',
           'annoy>=1.17.0,<2.0.0']}

setup_kwargs = {
    'name': 'ai-dataproc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nuxion',
    'author_email': 'nuxion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
