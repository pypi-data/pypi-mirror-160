# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ret']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ret = ret.__main__:main']}

setup_kwargs = {
    'name': 'ret',
    'version': '0.1.4',
    'description': 'A pure-python command-line regular expression tool for stream filtering, extracting, and parsing.',
    'long_description': '===\nRet\n===\n\n.. image:: https://codecov.io/gh/ThatXliner/ret/branch/master/graph/badge.svg?token=6B5AWYTL1O\n   :target: https://codecov.io/gh/ThatXliner/ret\n    \nA pure-python command-line regular expression tool for stream filtering, and extracting, designed to be minimal with an intuitive command-line interface.\n\nInstallation\n-------------\n\nYou can install this via\n\n.. code-block:: bash\n\n    $ python3 -m pip install ret\n    ✨🍰✨\n\n\nor using pipx\n\n.. code-block:: bash\n\n    $ pipx install ret\n    ✨🍰✨\n\nRet is pure python (tested on python 3.6+) with no dependencies.\n\nThat way, you can get a clean uninstall.\n\n.. note::\n\n\tIf you want to install the bleeding edge version of ret, right when it gets pushed to master, see `here <https://github.com/ThatXliner/ret/blob/master/CONTRIBUTING.md#development-installation>`_ for instructions.\n\n\n\nUsage\n------\n\nExample\n~~~~~~~~\n\nYou can use ``ret`` to extract text via regex capture groups:\n\n.. code-block:: bash\n\n    $ git branch\n    * master\n    $ git branch | ret "\\* (\\w+)" s --group 1\n    master\n\n...finding all occurrences of a pattern:\n\n.. code-block:: bash\n\n    $ ls | ret ".*\\.py" findall\n    foo.py\n    bar.py\n\nand even all occurrences of a pattern **with capture groups**:\n\n.. code-block:: bash\n\n    $ ls | ret "(.*)\\.py" findall --group 1\n    foo\n    bar\n\n\nWhile those may seem untypical use cases, I have found myself using ``Ret`` countless times.\n\nHere\'s a one-liner for uninstalling unnecessary stuff for ``pip``:\n\n.. code-block:: bash\n\n   $ pip list --not-required | ret ".+\\n.+\\n((?:\\n|.)+)" f -g 1 | ret "([^\\s]+)\\s+.+\\n" f -g 1 | xargs pip uninstall --yes\n\n\nAnother case\n~~~~~~~~~~~~\n\nImagine this: you have just downloaded a bunch of tarballs, and have ran\n\n.. code-block:: bash\n\n   for x in $(grep ".+\\.tar\\.gz"); do tar -xzf $x; done\n\nNow you just want to ``cd`` into all of the extracted files, run :code:`./configure && make && make install`.\n\nYou could use ``ret`` to get the names of the extracted files, just from the tarballs\' names. Like this:\n\n.. code-block:: bash\n\n   $ ls | grep ".+\\.tar\\.gz"\n   foo.tar.gz\n   bar.tar.gz\n   foobar.tar.gz\n   extractme.tar.gz\n\n\n   $ ls | ret "(.+)\\.tar\\.gz" f -g 1\n   foo\n   bar\n   foobar\n   extractme\n\n\nand with that combined, we can do\n\n.. code-block:: bash\n\n   $ for x in (ls | ret "(.+)\\.tar\\.gz" f -g 1); do {\n      cd $x &&\n      ./configure && make && make install &&\n      cd -}; done\n   ✨🍰✨\n\nA life saver.\n\n----\n\nAnd remember, this is python regex: a very powerful regular expression engine.\n\nThe possibilities of usage are endless.\n\nDemonstration\n~~~~~~~~~~~~~\n\n.. image:: https://raw.githubusercontent.com/ThatXliner/ret/master/assets/demo.svg\n   :alt: Demonstration photo\n\n\nBackground\n-------------\nI love ``grep``. But grep isn\'t really for text extraction.\n\nFor example, you cannot extract regexes via capture groups.\n\nSince I wanted that functionality, I decided to build this, ``Ret``.\n\nWhy the name?\n~~~~~~~~~~~~~\n\n``Ret`` is an acronym for **r**\\ egular **e**\\ xpression **t**\\ ool.\n\n\nWhy it can\'t replace grep\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n``Ret`` originally was designed to provide some features ``grep`` lacks.\nIt never intended to replace good ol\' ``grep``.\n\nGrep is great for searching directories while\n``ret`` (currently) can only read from a file or stdin.\n\nFurthermore, you cannot guarantee that ``ret`` is installed on the machine.\n\nAlso, ``Ret`` relies on the (slow) python regex engine.\n\nWhat about sed?\n~~~~~~~~~~~~~~~~\nSed is for find-and-replacing streams. Ret\'s different. But together, you can do some powerful things\n\n\nFeel free to contribute!\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ThatXliner/ret/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
