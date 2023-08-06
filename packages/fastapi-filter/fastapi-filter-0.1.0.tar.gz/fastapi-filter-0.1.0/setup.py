# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_filter',
 'fastapi_filter.base',
 'fastapi_filter.contrib',
 'fastapi_filter.contrib.mongoengine',
 'fastapi_filter.contrib.sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.78,<0.80', 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{'all': ['mongoengine>=0.24.1,<0.25.0', 'SQLAlchemy>=1.4.36,<2.0.0'],
 'mongoengine': ['mongoengine>=0.24.1,<0.25.0'],
 'sqlalchemy': ['SQLAlchemy>=1.4.36,<2.0.0']}

setup_kwargs = {
    'name': 'fastapi-filter',
    'version': '0.1.0',
    'description': 'FastAPI filter',
    'long_description': '[![pypi downloads](https://img.shields.io/pypi/dm/fastapi-filter?color=%232E73B2&logo=python&logoColor=%23F9D25F)](https://pypi.org/project/fastapi-filter)\n[![codecov](https://codecov.io/gh/arthurio/fastapi-filter/branch/main/graph/badge.svg?token=I1DVBL1682)](https://codecov.io/gh/arthurio/fastapi-filter)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/83451c4f-76dd-4154-9b2d-61f654eb0704/deploy-status)](https://fastapi-filter.netlify.app/)\n[![CodeQL](https://github.com/arthurio/fastapi-filter/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/arthurio/fastapi-filter/actions/workflows/codeql-analysis.yml)\n\n# FastAPI filter\n\n## Compatibilty\n\n**Required:**\n  * Python: 3.10+\n  * Fastapi: 0.78+\n  * Pydantic: 1.9+\n\n**Optional**\n  * MongoEngine: 0.24.1+\n  * SQLAlchemy: 1.4.36+\n\n## Installation\n\n```bash\n# Basic version\npip install fastapi-filter\n\n# With backends\npip install fastapi-filter[all]\n\n# More selective\npip install fastapi-filter[sqlalchemy]\npip install fastapi-filter[mongoengine]\n```\n\n## Documentation\n\nPlease visit: [https://fastapi-filter.netlify.app/](https://fastapi-filter.netlify.app/)\n\n## Examples\n\n![Swagger UI](https://raw.githubusercontent.com/arthurio/fastapi-filter/main/docs/swagger-ui.png)\n\nYou can play with examples:\n\n```bash\npip install poetry\npoetry install\npython examples/fastapi_filter_sqlalchemy.py\n```\n\n### Filter\n\nhttps://user-images.githubusercontent.com/950449/176737541-0e36b72f-38e2-4368-abfa-8bbc0c82e8ae.mp4\n\n### Order by\n\nhttps://user-images.githubusercontent.com/950449/176747056-ea82d6b9-cb3b-43eb-aec7-96ba0bc79e8b.mp4\n\n## Contribution\n\nYou can run tests with `pytest`.\n\n```bash\npip install poetry\npoetry install --extras all\npytest\n```\n\n<img width="884" alt="arthur_Arthurs-MacBook-Pro-2___code_fastapi-filter" src="https://user-images.githubusercontent.com/950449/176737623-a77f15d6-4e60-4c06-bdb7-b3d77f346a54.png">\n',
    'author': 'Arthur Rio',
    'author_email': 'arthur.rio44@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arthurio/fastapi-filter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
