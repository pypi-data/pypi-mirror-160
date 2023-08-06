# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wiktionary_de_parser', 'wiktionary_de_parser.methods']

package_data = \
{'': ['*'], 'wiktionary_de_parser': ['assets/*']}

install_requires = \
['lxml>=4.9.1,<5.0.0', 'mwparserfromhell>=0.6.4,<0.7.0']

setup_kwargs = {
    'name': 'wiktionary-de-parser',
    'version': '0.9.5',
    'description': 'Extracts data from German Wiktionary dump files. Allows you to add your own extraction methods 🚀',
    'long_description': '# wiktionary-de-parser\n\nThis is a Python module to extract data from German Wiktionary XML files (for Python 3.7+). It allows you to add your own extraction methods.\n\n## Installation\n\n`pip install wiktionary-de-parser`\n\n## Features\n\n- Extracts flexion tables, genus, IPA, language, lemma, part of speech (basic), syllables, raw Wikitext\n- Allows you to add your own extraction methods (pass them as argument)\n- Yields per section, not per page (a word can have multiple meanings --> multiple sections of a Wiktionary pages)\n\n## Usage\n\n```python\nfrom bz2 import BZ2File\nfrom wiktionary_de_parser import Parser\n\nbzfile_path = \'/tmp/dewiktionary-latest-pages-articles-multistream.xml.bz2\'\nbz_file = BZ2File(bzfile_path)\n\nfor record in Parser(bz_file):\n    if \'lang_code\' not in record or record[\'lang_code\'] != \'de\':\n      continue\n    # do stuff with \'record\'\n```\n\nNote: In this example we load a compressed Wiktionary dump file that was [obtained from here](https://dumps.wikimedia.org/dewiktionary/latest).\n\n### Adding new extraction methods\n\nAn extraction method takes the following arguments:\n\n- `title` (_string_): The title of the current Wiktionary page\n- `text` (_string_): The [Wikitext](https://en.wikipedia.org/wiki/Wiki#Editing) of the current word entry/section\n- `current_record` (_Dict_): A dictionary with all values of the current iteration (e. g. `current_record[\'lang_code\']`)\n\nIt must return a `Dict` with the results or `False` if the record was processed unsuccesfully.\n\n```python\n# Create a new extraction method\ndef my_method(title, text, current_record):\n  # do stuff\n  return {\'my_field\': my_data} if my_data else False\n\n# Pass a list with all extraction methods to the class constructor:\nfor record in Parser(bz_file, custom_methods=[my_method]):\n    print(record[\'my_field\'])\n```\n\n## Output\nExample output for the word "Abend":\n```python\n{\'flexion\': {\'Akkusativ Plural\': \'Abende\',\n             \'Akkusativ Singular\': \'Abend\',\n             \'Dativ Plural\': \'Abenden\',\n             \'Dativ Singular\': \'Abend\',\n             \'Genitiv Plural\': \'Abende\',\n             \'Genitiv Singular\': \'Abends\',\n             \'Genus\': \'m\',\n             \'Nominativ Plural\': \'Abende\',\n             \'Nominativ Singular\': \'Abend\'},\n \'inflected\': False,\n \'ipa\': [\'ˈaːbn̩t\', \'ˈaːbm̩t\'],\n \'lang\': \'Deutsch\',\n \'lang_code\': \'de\',\n \'lemma\': \'Abend\',\n \'pos\': {\'Substantiv\': []},\n \'rhymes\': [\'aːbn̩t\'],\n \'syllables\': [\'Abend\'],\n \'title\': \'Abend\'}\n```\n\n## Development\nThis project uses [Poetry](https://python-poetry.org/).\n\n1. Install [Poetry](https://python-poetry.org/).\n2. Clone this repository\n3. Run `poetry install` inside of the project folder to install dependencies.\n4. Change `wiktionary_de_parser/run.py` to your needs.\n5. Run `poetry run python wiktionary_de_parser/run.py` to run the parser. Or `poetry run pytest` to run tests.\n\n## License\n\n[MIT](https://github.com/gambolputty/wiktionary-de-parser/blob/master/LICENSE.md) © Gregor Weichbrodt\n',
    'author': 'Gregor Weichbrodt',
    'author_email': 'gregorweichbrodt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gambolputty/wiktionary-de-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
