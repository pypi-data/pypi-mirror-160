# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noxcollections']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noxcollections',
    'version': '0.2.0.dev1',
    'description': 'Pure python implementation of simple data structures and some basic algorithms focused on readability.',
    'long_description': "noxcollections\n==============\n\nsimple, clean, pure python collections\n---------------------------------------\n\n**noxcollections** is pure Python implementation of basic data structures and a\nfew basic algorithms operating on them.\n\nDisclaimer\n==========\n\nThis project's main purpose is to get myself acquainted to the process of\ndeveloping a proper python package with the common tooling used for testing,\nlinting, type checking, and building in python.\n\nAdditionally I hope to refresh and better structure my knowledge about the\nimplemented data structures and algorithms.\n\nFor the reasons stated above this project is mainly meant for educational\npurposes. **If you need performance built-in package** ``collections`` **as well\nas some other packages from PyPI will probably serve you better** (due to better\noptimization as well as the fact that most of them are implemented as C\nextensions).\n\nGoals\n=====\n\nFollowing goals are most important to this project:\n\n- Clean, modern code\n- Full test coverage\n- Fully typed public API\n\nCurrent state\n=============\n\nThe following lists contain planned features and their state current state.\n\nThis package is currently before its first release. \n\nData structures\n---------------\n\n- [ ] Linked lists and other data structures that can be based on them\n    - [x] Linked list\n    - [ ] Doubly linked list\n    - [x] Stack\n    - [ ] Queues\n- [ ] Other list types\n- [ ] Tree based structures\n- [ ] Graphs based structures\n\nAlgorithms\n----------\n\n- [x] Search Algorithms\n    - [x] Binary search\n- [ ] Sorting Algorithms\n    - [ ] Bubble sort\n    - [ ] Merge sort \n    - [ ] Quick sort\n- [ ] Graph algorithms (TBD)\n\nHow to use\n==========\n\nFor use only Python(``3.8+``) interpreter is needed. To run test/linters/mypy\nuse of Poetry_ is recommended. Further instructions will assume you have it \ninstalled.\n\n.. _Poetry: https://python-poetry.org/\n\nInstallation\n------------\n\nInstall using pip\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nYou can install last release version of this package from PyPI_ using ``pip``.\n\n.. code-block:: bash\n\n    pip install noxcollections\n\n.. _PyPi: https://pypi.org/project/noxcollections/\n\nUsing Poetry\n------------\n\nFirst install the package in the environment manage by Poetry:\n\n.. code-block:: bash\n\n    poetry install  # build, from main repository directory\n\nAnd then call your script from the main repository's directory prefacing it \nwith ``poetry`` for example if your file is int same directory and as called\n``main.py``::\n\n    poetry python main.py\n\nTesting and linting\n===================\n\nTesting uses the pytest_ package for testing and tox_ to run the test suite\nagainst multiple versions of Python:\n\n- ``3.8``\n- ``3.9``\n- ``3.10``\n\nTox configurations also does linting (using black_ and flake8_) and type\nchecking (using mypy_)\n\nTo run all of the aforementioned tools using tox (after installing all of the \ndependencies and package using ``poetry install``)::\n\n    poetry run tox\n\nTo run those tools more selectively check the ``tox.ini`` file to check the names\nof the environments you wish to run.\n\n.. _pytest: https://pytest.org/\n.. _tox: https://tox.wiki/\n.. _black: https://pypi.org/project/black/\n.. _flake8: https://flake8.pycqa.org/\n.. _mypy: http://www.mypy-lang.org/",
    'author': 'Marcin Śladewski',
    'author_email': 'mar4sladewski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NoxMar/noxcollections',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
