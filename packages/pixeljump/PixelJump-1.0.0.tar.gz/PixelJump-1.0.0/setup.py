# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pixeljump', 'pixeljump.levels']

package_data = \
{'': ['*'],
 'pixeljump': ['assets/*',
               'assets/TILES/*',
               'assets/TILES2/*',
               'assets/TILES3/*',
               'assets/alien1_flying/*',
               'assets/alien2_idle/*',
               'assets/alien2_walking/*',
               'assets/dragon/*',
               'assets/froggy_idle/*',
               'assets/froggy_walking/*',
               'assets/idle/*',
               'assets/jumping/*',
               'assets/layers/act1/*',
               'assets/layers/act2/*',
               'assets/layers/act3/*',
               'assets/maps/*',
               'assets/marine_idle/*',
               'assets/marine_running/*',
               'assets/mushroom_idle/*',
               'assets/mushroom_walking/*',
               'assets/music/*',
               'assets/nightmare/*',
               'assets/particle/*',
               'assets/projectile/*',
               'assets/rain_particle/*',
               'assets/rocket_particle/*',
               'assets/running/*',
               'settings/*']}

install_requires = \
['lizard>=1.17.10,<2.0.0',
 'pygame-widgets>=1.0.0,<2.0.0',
 'pygame>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['pixeljump = pixeljump.main:main']}

setup_kwargs = {
    'name': 'pixeljump',
    'version': '1.0.0',
    'description': 'NUS Orbital 21/22 Team PixelJump',
    'long_description': "# NUS Orbital 21/22 Team PixelJump (5215)\n\n![Tests](https://github.com/WilsonOh/Orbital21-22-PixelJump-5215/actions/workflows/tests.yml/badge.svg)\n\n## Game Instructions\n- `A` and `D` to move left/right\n- `space` to jump/double-jump\n- In Act 2 & 3 press and hold `space` after a double jump to activate rocket boots 🚀\n- In Act 3 press `P` to shoot projectiles to kill enemies 🔫  \n- M to mute all sounds and music 🔇\n- Escape to pause the game ⏸️\n\nIn the main menu, in addition to `enter` you can press the buttons `1`, `2` or `3` to go straight to acts 1, 2 and 3 respectively if you don't feel like beating the game normally 💀\n\n## Running the game\n### Option 1: Run the packaged executable (reccomended for windows users)\nGo to [releases](https://github.com/WilsonOh/Orbital21-22-PixelJump-5215/releases/tag/v1.0.0) and follow the instructions for your OS.<br>\nThe packaged executables are only tested on limited hardware so there may be some problems that we have not faced.<br>\nIf the executable packages do not work, then the most reliable way is to run the program from source, which will be explained below.\n\n### Option 2: Install using pip (reccomended in general if you have python >= 3.10 installed)\n1. execute `pip install pixeljump` for the stable release or `pip install git+https://github.com/WilsonOh/Orbital21-22-PixelJump-5215.git` for the nightly release\n2. run the game with `pixeljump`\n\n### Option 3.a: Running from source using `pip` (not reccomended)\n1. Make sure you have `python3.10` installed. You can download and install it from https://www.python.org/downloads/\n2. Clone the repo and `cd` into it\n3. Create a python `venv`<sup>[1]</sup>\n4. run `pip install pygame pygame-widgets` and `pip install -e .`\n5. `cd src/pixeljump` and `python3 main.py`\n\n### Option 3.b: Running from source using `poetry`\nIf you have [poetry](https://python-poetry.org/) installed, it will be easier since this project uses poetry\n1. `cd pixeljump` and run `poetry install`\n2. `cd src/pixeljump` and run `poetry shell`\n3. Run the game with `python main.py`\n\n[1] Create a `venv` by running `python3 -m venv venv`\n\n### Configuring Game Settings\nAll the configurable settings are stored in the `settings/settings.json` file in the game folder.<br>\nSince the current version of `PIXELJUMP` does not support in-game settings configuration yet, the only way to adjust the game settings is to edit the `settings.json` file.\n#### Screen Resolution\nThe game is in `1920x1080` by default as it was the resolution we had in mind when designing the game but you can change it to your liking.<br>\nThe screen resolution of the game can be changed by adjusting the `screen_width` and `screen_height` keys in `settings.json`\n#### FPS\nIt is not reccomended to change the FPS as it may cause some unwanted behaviours\n#### Player velocity and gravity\nFeel free to mess around with the velocity and gravity of the player :smile:\n\n\n### Project Poster\n![project_poster](https://drive.google.com/uc?export=view&id=1IXPpNm3-gM2gn9Cc_cCF63Dolu9mMFPT)\n",
    'author': 'Wilson Oh',
    'author_email': 'e0773510@u.nus.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WilsonOh/Orbital21-22-PixelJump-5215',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
