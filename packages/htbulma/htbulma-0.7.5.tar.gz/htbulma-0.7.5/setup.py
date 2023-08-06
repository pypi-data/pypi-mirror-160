# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htbulma', 'htbulma.services']

package_data = \
{'': ['*']}

install_requires = \
['htag>=0.7,<0.8']

setup_kwargs = {
    'name': 'htbulma',
    'version': '0.7.5',
    'description': 'GUI toolkit for creating beautiful applications for mobile, web, and desktop from a single python3 codebase',
    'long_description': '## htbulma = "HTag bulma"\n\nExemple of gui toolkit using [htag](https://github.com/manatlan/htag).\n\n[available on pypi](https://pypi.org/project/htbulma/)\n\n**Just to be clear** : This module is just for me ;-). It\'s just here to demonstrate that you can build a py3 module, containnig a set of [htag](https://github.com/manatlan/htag)\'s components, ready to be used, in you [htag](https://github.com/manatlan/htag) app.\n\nOf course, you can use it, at your own risk. But be aware that :\n\n * the current components may change completly (and broke your apps)\n * many of them are not well coded (80% coming from the old gtag, and 70% are not using the last htag features in the right place)\n \nTheses are my components, for my quick\'s htag apps ;-), for demo\'ing the htag goal !\n\nI\'d love too see a real module, well maintained, with high-end and clever components (but I have no time to manage that, focusing on other projects (ex: htag))\n\n[See an example](test.py)\n',
    'author': 'manatlan',
    'author_email': 'manatlan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manatlan/htbulma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
