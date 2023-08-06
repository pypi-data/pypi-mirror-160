# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interactive_system_magic']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.4.0,<9.0.0', 'pexpect>=4.6.0,<5.0.0']

setup_kwargs = {
    'name': 'interactive-system-magic',
    'version': '0.2.0',
    'description': 'An IPython magic to run system commands interactively',
    'long_description': '.. SPDX-FileCopyrightText: © 2022 Matt Williams <matt@milliams.com>\n   SPDX-License-Identifier: MIT\n\nRun interactive commands with IPython/Jupyter\n=============================================\n\nSetup\n-----\n\nFirst, you need to load the extension with:\n\n.. code-block:: ipython\n\n    %load_ext interactive_system_magic\n\nNow, you can start using it.\n\nRunning programs\n----------------\n\nIf you make a code cell with:\n\n.. code-block:: ipython\n\n    %prog echo blah\n\nthen it will run the program ``echo blah`` and put the result in the output:\n\n.. code-block::\n\n    blah\n\nSo far, this is just like the ``!`` system call syntax.\nHowever, it also allows you to send input into a program by using it in cell mode:\n\n.. code-block:: ipython\n\n    %%prog bc --quiet\n    1+1\n\nwhich will call ``bc --quiet`` (the ``--quiet`` part is to suppress the info on startup) and then pass in ``1+1`` on the stdin.\n``bc`` will read this and output the result:\n\n.. code-block::\n\n    2\n\nIf you want to use this to demonstrate what the user would see if they ran this manually on a terminal,\ni.e. to include the input as well as the output, you can use the interactive ``-i`` flag:\n\n.. code-block:: ipython\n\n    %%prog -i bc --quiet\n    1+1\n\nwhich gives:\n\n.. code-block::\n\n    1+1\n    2\n\nFinally, if you want to be able to respond to prompts in the program\'s output,\nthen you can use special syntax to specify the prompt you are looking for, and the thing to respond to it with.\nIn this case, we are calling the ``python`` program and waiting for its ``>>>`` prompt and then sending ``print("hello")``\n\n.. code-block:: ipython\n\n    %%prog -i -d [] python -q\n    [>>> ]print("hello")\n\nwhich gives:\n\n.. code-block::\n\n    >>> print("hello")\n    hello\n    >>>\n\nRun Python scripts\n------------------\n\nAs a shortcut, you can also run any Python scripts you have using the same interpreter that IPython or the Jupyter notebook is running with.\nIf you make a Python script with (or use an existing one of course):\n\n.. code-block:: ipython\n\n    %%writefile foo.py\n\n    print("This is a script")\n\nyou can call it with:\n\n.. code-block:: ipython\n\n    %run_python_script foo.py\n\nand get:\n\n..code-block::\n\n    This is a script\n\nThis magic supports the same cell-mode commands and interactive options as ``%%prog``.\n',
    'author': 'Matt Williams',
    'author_email': 'matt@milliams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/milliams/interactive-system-magic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
