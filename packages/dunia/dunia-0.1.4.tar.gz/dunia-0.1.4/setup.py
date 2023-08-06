# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunia',
 'dunia.lexbor',
 'dunia.log',
 'dunia.lxml',
 'dunia.modest',
 'dunia.playwright']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=4.0.2,<5.0.0',
 'backoff>=2.1.2,<3.0.0',
 'charset-normalizer>=2.1.0,<3.0.0',
 'cssselect>=1.1.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.9.1,<5.0.0',
 'playwright>=1.23.1,<2.0.0',
 'selectolax>=0.3.7,<0.4.0',
 'throttler>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'dunia',
    'version': '0.1.4',
    'description': 'HTML parsing of JavaScript heavy websites using multiple backends (lxml, modest, playwright, etc.).',
    'long_description': 'MIT License\n\nCopyright (c) 2022 Danyal Zia Khan\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Danyal Zia Khan',
    'author_email': 'danyal6870@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
