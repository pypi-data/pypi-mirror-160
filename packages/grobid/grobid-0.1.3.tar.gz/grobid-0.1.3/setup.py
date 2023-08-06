# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grobid', 'grobid.models']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'httpx>=0.23.0,<0.24.0', 'lxml>=4.9.1,<5.0.0']

extras_require = \
{'json': ['mashumaro>=3.0.3,<4.0.0']}

setup_kwargs = {
    'name': 'grobid',
    'version': '0.1.3',
    'description': 'Python library for serializing GROBID TEI XML to dataclass',
    'long_description': '# grobid\n> Python library for serializing GROBID TEI XML to [dataclasses](https://docs.python.org/3/library/dataclasses.html)\n\n[![Build Status](https://github.com/ram02z/grobid/workflows/tests/badge.svg)](https://github.com/ram02z/grobid/actions)\n[![Coverage Status](https://coveralls.io/repos/github/ram02z/grobid/badge.svg)](https://coveralls.io/github/ram02z/grobid)\n[![Latest Version](https://img.shields.io/pypi/v/grobid.svg)](https://pypi.python.org/pypi/grobid)\n[![Python Version](https://img.shields.io/pypi/pyversions/grobid.svg)](https://pypi.python.org/pypi/grobid)\n[![License](https://img.shields.io/badge/MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\n## Installation\n\nUse `pip` to install:\n\n```shell\n$ pip install grobid\n$ pip install grobid[json] # for JSON serializable dataclass objects\n```\n\n\nYou can also download the `.whl` file from the release section:\n\n```shell\n$ pip install *.whl\n```\n\n## Usage\n\n### Client\n\nIn order to convert an academic PDF to TEI XML file, we use GROBID\'s REST\nservices. Specifically the [processFulltextDocument](https://grobid.readthedocs.io/en/latest/Grobid-service/#apiprocessfulltextdocument) endpoint.\n\n\n```python\nfrom pathlib import Path\nfrom grobid.models.form import Form, File\nfrom grobid.models.response import Response\n\npdf_file = Path("<your-academic-article>.pdf")\nwith open(pdf_file, "rb") as file:\n    form = Form(\n        file=File(\n            payload=file.read(),\n            file_name=pdf_file.name,\n            mime_type="application/pdf",\n        )\n    )\n    c = Client(base_url="<base-url>", form=form)\n    try:\n        xml_content = c.sync_request().content  # TEI XML file in bytes\n    except GrobidClientError as e:\n        print(e)\n```\n\nwhere `base-url` is the URL of the GROBID REST service\n\n> You can use `https://cloud.science-miner.com/grobid/` to test\n\n#### [Form](https://github.com/ram02z/grobid/blob/master/src/grobid/models/form.py#L20)\n\nThe `Form` class supports most of the optional parameters of the processFulltextDocument\nendpoint.\n\n\n### Parser\n\nIf you want to serialize the XML content, we can use the `Parser` class to\ncreate [dataclasses](https://docs.python.org/3/library/dataclasses.html)\nobjects.\n\nNot all of the GROBID annoation guidelines are met, but compliance is a goal.\nSee [#1](https://github.com/ram02z/grobid/issues/1).\n\n```python\nfrom grobid.tei import Parser\n\nxml_content: bytes\nparser = Parser(xml_content)\narticle = parser.parse()\narticle.to_json()  # throws RuntimeError if extra require \'json\' not installed\n```\n\nwhere `xml_content` is the same as in [Client section](#client)\n\nAlternately, you can load the XML from a file:\n\n```python\nfrom grobid.tei import Parser\n\nwith open("<your-academic-article>.xml", "rb") as xml_file:\n  xml_content = xml_file.read()\n  parser = Parser(xml_content)\n  article = parser.parse()\n  article.to_json()  # throws RuntimeError if extra require \'json\' not installed\n```\n\nWe use [mashumaro](https://github.com/Fatal1ty/mashumaro) to serialize the\ndataclasses into JSON (mashumaro supports other formats, you can submit a PR if\nyou want). By default, mashumaro isn\'t installed, use `pip install\ngrobid[json]`.\n\n## License\n\nMIT\n\n## Contributing\n\nYou are welcome to add missing features by submitting a PR, however, I won\'t be\naccepting any requests other than GROBID annotation compliance.\n\n## Disclaimer\n\nThis module was originally part of a group university project, however, all the\ncode and tests was also authored by me.\n',
    'author': 'Omar Zeghouani',
    'author_email': 'omarzeghouanii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ram02z/grobid',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
