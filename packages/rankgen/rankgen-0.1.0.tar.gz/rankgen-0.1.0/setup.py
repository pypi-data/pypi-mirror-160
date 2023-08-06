# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rankgen', 'rankgen.parallel']

package_data = \
{'': ['*'], 'rankgen.parallel': ['parallel_logs/*', 'parallel_schedulers/*']}

install_requires = \
['gdown>=4.5.1,<5.0.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'torch>=1.12.0,<2.0.0',
 'transformers>=4.20.1,<5.0.0']

setup_kwargs = {
    'name': 'rankgen',
    'version': '0.1.0',
    'description': 'RankGen is a suite of encoder models (100M-1.2B parameters) which map prefixes and generations from any pretrained English language model to a shared vector space. RankGen can be used to rerank multiple full-length samples from an LM, and it can also be incorporated as a scoring function into beam search to significantly improve generation quality (0.85 vs 0.77 MAUVE, 75% preference according to humans annotators who are English writers).',
    'long_description': None,
    'author': 'Kalpesh Krishna, Yapei Chang, John Wieting, Mohit Iyyer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
