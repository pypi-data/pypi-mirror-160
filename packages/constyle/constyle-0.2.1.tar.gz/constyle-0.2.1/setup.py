# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['constyle']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.11.0,<5.0.0']

entry_points = \
{'console_scripts': ['constyle = constyle.__main__:main']}

setup_kwargs = {
    'name': 'constyle',
    'version': '0.2.1',
    'description': 'A Python library to add style to your console.',
    'long_description': '# constyle\nA Python library to add style to your console.\n\nThe name of the library comes from merging the words **CONSoLE** and **STYLE**.\n\n## Installation\n\nYou can install this package with pip or conda.\n```sh\n$ pip install constyle\n```\n```sh\n$ conda install -c abrahammurciano constyle\n```\n\n## Links\n\nThe full documentation is available [here](https://abrahammurciano.github.io/python-constyle/constyle).\n\nThe source code is available [here](https://github.com/abrahammurciano/python-constyle).\n\n## Usage\n\nThere are a couple of ways to use this library.\n\n### The `style` function\n\nThe simplest way is with the `style` function.\n\n```py\nfrom constyle import style, Attributes\n\nprint(style(\'Hello World\', Attributes.GREEN, Attributes.BOLD, Attributes.ON_BLUE))\n```\n\n### `Attribute` objects\n\n`Attribute` objects are all callable, and calling them will apply their style to the given input string.\n\n```py\nfrom constyle import Attributes\n\nunderline = Attributes.UNDERLINE\nprint(underline("You wanna experience true level? Do you?"))\n```\n\n### `Style` objects\n\nYou can also use `Style` objects to create a reusable style with several attributes. `Style` objects are callable and take a string as input and return a styled string.\n\nAdding together `Attribute` objects will also create `Style` objects, as will adding `Attribute`s to existing `Style` objects.\n\n```py\nfrom constyle import Style, Attributes\n\nwarning = Style(Attributes.YELLOW, Attributes.BOLD)\nwhisper = Attributes.GREY + Attributes.DIM + Attributes.SUPERSCRIPT\n\nprint(warning(\'You shall not pass!\'))\nprint(whisper(\'Fly you fools\'))\n```\n\n### Attributes\n\nThe `Attributes` enum contains all the available ANSI attributes. You can read more about them [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).\n\nYou\'ll find there is limited support for all the ANSI attributes among consoles.\n\nIf you need more attributes than the ones provided in this enum, you can create your own by using the `Attribute` class.\n\n### Nesting\n\nNesting strings is not supported. The inner string will cause the rest of the outer string to lose its formatting.\n\n> NOTE: I would like to implement a fix for this in future, but I am uncertain if it is even possible, let alone feasible. If you have any suggestions, feel free to open an issue.\n\n```py\nfrom constyle import Attributes\n\nbold = Attributes.BOLD\nyellow = Attributes.YELLOW\ngreen = Attributes.GREEN\n\nprint(yellow(bold(\'This is bold and yellow\')))\nprint(green(f"This is green. {yellow(\'This is yellow.\')} This is no longer green"))\n```\n\n### RGB and 8-bit colours\n\nYou can create an attribute for whichever colour you want with the classes `ForegroundRGB`, `BackgroundRGB` and `Foreground8Bit` and `Background8Bit`. For example:\n\n```py\nfrom constyle import ForegroundRGB, style\n\nprint(style("This is a pink string", ForegroundRGB(255, 128, 255)))\n```\n\n### The command line interface\n\nThis package also provides a very basic command line interface to print styled strings.\n\nUse `constyle --help` to see how to use it.',
    'author': 'Abraham Murciano',
    'author_email': 'abrahammurciano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahammurciano/python-constyle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
