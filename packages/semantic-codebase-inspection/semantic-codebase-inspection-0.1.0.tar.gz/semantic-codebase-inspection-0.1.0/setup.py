# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantic_codebase_inspection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'semantic-codebase-inspection',
    'version': '0.1.0',
    'description': 'Semantic Codebase Inspection helps developers familiarize themselves with a python project that has decent naming conventions. Dependencies not included.',
    'long_description': "# Semantic Codebase Inspection\n\nSCI helps developers familiarize themselves with a python project that has decent naming conventions.\n\nIt requires the libraries: \n\ntensorflow-text\ntensorflow-hub\ninspect\n\nIt downloads an NLP model of about 300MB.\n\nhttps://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3\n\nIt uses a Natural Language Processing model to turn the names of functions, classes, and variables (variables that outside of functions) into vectors. Queries can be submitted against those names which don't need to be exact matches. Currently, the language model being used accommodates 16 languages, which means it accommodates synonyms too. This is accomplished with technology related to word2vec, doc2vec, and embeddings. If this seems somehow magic to you, I encourage you to read more about it so that you can be a magician too because it's not that complicated.\n\n```python3\n>> import semantic_codebase_inspection\n>> semantic_codebase_inspection.run_semantic_search_through_program()\n(printed) Importing modules and semantic model.\n\n(printed) What module would you like to explore?\n(input) requests\n\n(printed) What function in the library are you interesting in exploring?\n(input) get\n\n(printed) How many objects would you like in your result? (integer answers only)\n(input) 5\n\n*waiting for search to execute*\n\nSimilar semantic candidates include:\nget : get function\nput : put function\n__build__ :   build   int \n__url__ :   url   str \npost : post function\n```\n\nExit with ctrl+C.",
    'author': 'mandrewstuart',
    'author_email': 'andrew_matte_@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
