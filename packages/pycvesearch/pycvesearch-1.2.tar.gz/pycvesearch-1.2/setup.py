# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycvesearch']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pycvesearch',
    'version': '1.2',
    'description': 'Python API for CVE search.',
    'long_description': '[![Python application](https://github.com/cve-search/PyCVESearch/actions/workflows/mypy.yml/badge.svg)](https://github.com/cve-search/PyCVESearch/actions/workflows/mypy.yml)\n\n**Important Note**: The API search endpoint has been removed from the public instance due to massive abusive behavior. You can use this API against a local version of CVE Search.\n\n**PyCVESearch** is an easy to use wrapper around cve-search. Some of the calls will work against https://cve.circl.lu but for most of them, you need your own CVE Search instance. For the ones available on the public instance, see https://github.com/cve-search/PyCVESearch/blob/main/tests/tests.py.\n\nThis library is based on the work of [Martin Simon](https://github.com/mrsmn/ares) and [Kai Renken](https://github.com/elektrischermoench/ares3).\n\n\n## Installation:\n\nFrom source use\n\n```\n    $ pip install pycvesearch\n```\n\n## Documentation:\n\n- **`GET /api/browse/`**\n- **`GET /api/browse/vendor`**\n\n```python\n>>> from pycvesearch import CVESearch\n>>> cve = CVESearch()\n>>> cve.browse(<vendor>)\n```\n\n- **`GET /api/search/vendor/product`**\n\n```python\n>>> cve.search(\'microsoft/office\')\n```\n\n- **`GET /api/cveid/cveid`**\n\n```python\n>>> cve.id(\'CVE-2014-0160\')\n```\n\n- **`GET /api/last`**\n\n```python\n>>> cve.last()\n```\n\n- **`GET /api/dbInfo`**\n\n```python\n>>> cve.dbinfo()\n```\n\n- **`GET /api/cpe2.2/cpe`**\n\n```python\n>>> cve.cpe22(\'cpe:/a:microsoft:office:2011::mac\')\n```\n\n- **`GET /api/cpe2.3/cpe`**\n\n```python\n>>> cve.cpe23(\'cpe:2.3:a:microsoft:office:2011:-:mac\')\n```\n\n- **`GET /api/cvefor/cpe`**\n\n```python\n>>> cve.cvefor(\'cpe:/a:microsoft:office:2011::mac\')\n```\n\n## License:\n\n```\n    Apache v2.0 License\n    Copyright 2015-2016 Martin Simon\n    Copyright 2015-2016 Kai Renken\n    Copyright 2016 Raphaël Vinot\n\n     Licensed under the Apache License, Version 2.0 (the "License");\n     you may not use this file except in compliance with the License.\n     You may obtain a copy of the License at\n\n         http://www.apache.org/licenses/LICENSE-2.0\n\n     Unless required by applicable law or agreed to in writing, software\n     distributed under the License is distributed on an "AS IS" BASIS,\n     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n     See the License for the specific language governing permissions and\n     limitations under the License.\n\n```\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cve-search/PyCVESearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
