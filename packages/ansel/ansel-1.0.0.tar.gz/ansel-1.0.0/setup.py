# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansel', 'ansel.encodings']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['Sphinx', 'sphinx-rtd-theme<1']}

setup_kwargs = {
    'name': 'ansel',
    'version': '1.0.0',
    'description': 'Codecs for reading/writing documents in the ANSEL character set.',
    'long_description': '============\nANSEL Codecs\n============\n\n\n.. image:: https://img.shields.io/pypi/v/ansel.svg\n        :target: https://pypi.python.org/pypi/ansel\n        :alt: PyPI Status\n\n.. image:: https://github.com/haney/python-ansel/actions/workflows/build.yml/badge.svg\n        :target: https://travis-ci.org/haney/python-ansel\n        :alt: Build Status\n\n.. image:: https://readthedocs.org/projects/python-ansel/badge/?version=latest\n        :target: https://python-ansel.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nCodecs for reading/writing documents in the ANSEL character set.\n\n\n* Free software: MIT license\n* Documentation: https://python-ansel.readthedocs.io.\n\n\nFeatures\n--------\n\n* Adds support for character set encodings ANSEL_ (ANSI/NISO Z39.47) and GEDCOM_.\n* Re-orders combining characters for consistency with the ANSEL specification.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n.. _ANSEL: https://en.wikipedia.org/wiki/ANSEL\n.. _GEDCOM: https://en.wikipedia.org/wiki/GEDCOM\n',
    'author': 'David Haney',
    'author_email': 'david.haney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/haney/python-ansel/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
