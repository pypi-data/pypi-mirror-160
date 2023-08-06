# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dndfog']

package_data = \
{'': ['*']}

install_requires = \
['pygame==2.1.2', 'pywin32==304']

entry_points = \
{'console_scripts': ['dndfog = dndfog.main:start']}

setup_kwargs = {
    'name': 'dndfog',
    'version': '0.2.0',
    'description': 'DND battle map with fog of war',
    'long_description': '# DnD Fog\n\n[![Coverage Status][coverage-badge]][coverage]\n[![GitHub Workflow Status][status-badge]][status]\n[![PyPI][pypi-badge]][pypi]\n[![GitHub][licence-badge]][licence]\n[![GitHub Last Commit][repo-badge]][repo]\n[![GitHub Issues][issues-badge]][issues]\n[![Python Version][version-badge]][pypi]\n\n```shell\npip install dndfog\n```\n\n---\n\n**Documentation**: [https://mrthearman.github.io/dndfog/](https://mrthearman.github.io/dndfog/)\n\n**Source Code**: [https://github.com/MrThearMan/dndfog/](https://github.com/MrThearMan/dndfog/)\n\n---\n\nCreate battlemaps for tabletop RPGs, like [D&D](https://www.dndbeyond.com/).\n\n> Program is Windows only for now. This is due to the saving and loading widgets\n> being Windows only (using pywin32). You\'re free to modify the code to add file\n> loading and saving for other platforms.\n\n![Example Map](https://github.com/MrThearMan/dndfog/blob/main/docs/img/example-map.png?raw=true)\n\n## Features\n\n- Infinite grid\n- Add and remove a "[fog of war](https://en.wikipedia.org/wiki/Fog_of_war)" effect\n- Import maps from image files\n- Place, move and remove pieces on a grid (can be matched to image grid)\n- Place 1x1, 2x2, 3x3, or 4x4 pieces\n- Save and load file to JSON files (background image saved in the JSON file!)\n\n## How to use\n\nWhen installing from [pypi](https://pypi.org/), the library should come with a script\nnamed `dndfog` that you can run. It should be available in your environment if\nthe `Python\\Scripts` folder is set in PATH. You can also download an EXE from\nthe [GitHub releases](https://github.com/MrThearMan/dndfog/releases).\n\nWhen the program opens, you need to select an image file to use as a background,\nor a JSON data file to load a map from. You can also lauch the program with extra\narguments `--file=<filepath>` or `--gridsize=<size>` to change the opening parameters.\n\n> The program does not autosave! You have to save (and override) the file yourself!\n\n### Keyboard shortcuts\n\n- Remove fog: `CTRL + Left mouse button`\n- Add fog: `CTRL + Shift + Left mouse button`\n- Add a piece: `Right mouse button`\n- Remove a piece: `Double click: Right mouse button`\n- Move a piece: `Click and drag: Left mouse button`\n- Move camera: `Click and drag: Middle mouse button`\n- Move background map: `ALT + Click and drag: Left mouse button`\n- Zoom in: `Scroll wheel: Up`\n- Zoom out: `Scroll wheel: Down`\n- Select 1x1 piece placement: `1`\n- Select 2x2 piece placement: `2`\n- Select 3x3 piece placement: `3`\n- Select 4x4 piece placement: `4`\n- Show/hide fog: `F1`\n- Show/hide grid: `F12`\n- Save file: `CTRL + s`\n- Open file: `CTRL + o`\n- Quit program: `Esc`\n\n## Known issues or lacking features\n\nWhen zooming, the program grid and background map might not stay aligned,\nif you have moved the background map. This is due to the background map offset\nnot being scaled correctly to the new zoom level. Usually this should be only\na few pixels, and you can fix it quickly by moving the background.\n\nGridsize can only be changed on initial lauch. Use the `--gridsize=<size>`\nextra argument on first lauch to change the grid size, and when you get it\ncorrect, save the file. There was some alignment issues with the background\nmap when I tried adding this, so I skipped it for now. Might add later.\n\nThere is no undo or redo. Might add later.\n\nThere is no way to mark/point on things on the map (apart from the mouse cursor).\nMight add later.\n\n[coverage-badge]: https://coveralls.io/repos/github/MrThearMan/dndfog/badge.svg?branch=main\n[status-badge]: https://img.shields.io/github/workflow/status/MrThearMan/dndfog/Test\n[pypi-badge]: https://img.shields.io/pypi/v/dndfog\n[licence-badge]: https://img.shields.io/github/license/MrThearMan/dndfog\n[repo-badge]: https://img.shields.io/github/last-commit/MrThearMan/dndfog\n[issues-badge]: https://img.shields.io/github/issues-raw/MrThearMan/dndfog\n[version-badge]: https://img.shields.io/pypi/pyversions/dndfog\n[loc-badge]: https://img.shields.io/tokei/lines/github.com/MrThearMan/dndfog\n[downloads-badge]: https://img.shields.io/pypi/dm/dndfog\n\n[coverage]: https://coveralls.io/github/MrThearMan/dndfog?branch=main\n[status]: https://github.com/MrThearMan/dndfog/actions/workflows/test.yml\n[pypi]: https://pypi.org/project/dndfog\n[licence]: https://github.com/MrThearMan/dndfog/blob/main/LICENSE\n[repo]: https://github.com/MrThearMan/dndfog/commits/main\n[issues]: https://github.com/MrThearMan/dndfog/issues\n',
    'author': 'Matti Lamppu',
    'author_email': 'lamppu.matti.akseli@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mrthearman.github.io/dndfog/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
