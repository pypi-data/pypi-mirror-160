# NUS Orbital 21/22 Team PixelJump (5215)

![Tests](https://github.com/WilsonOh/Orbital21-22-PixelJump-5215/actions/workflows/tests.yml/badge.svg)

## Game Instructions
- `A` and `D` to move left/right
- `space` to jump/double-jump
- In Act 2 & 3 press and hold `space` after a double jump to activate rocket boots 🚀
- In Act 3 press `P` to shoot projectiles to kill enemies 🔫  
- M to mute all sounds and music 🔇
- Escape to pause the game ⏸️

In the main menu, in addition to `enter` you can press the buttons `1`, `2` or `3` to go straight to acts 1, 2 and 3 respectively if you don't feel like beating the game normally 💀

## Running the game
### Option 1: Run the packaged executable (reccomended for windows users)
Go to [releases](https://github.com/WilsonOh/Orbital21-22-PixelJump-5215/releases/tag/v1.0.0) and follow the instructions for your OS.<br>
The packaged executables are only tested on limited hardware so there may be some problems that we have not faced.<br>
If the executable packages do not work, then the most reliable way is to run the program from source, which will be explained below.

### Option 2: Install using pip (reccomended in general if you have python >= 3.10 installed)
1. execute `pip install pixeljump` for the stable release or `pip install git+https://github.com/WilsonOh/Orbital21-22-PixelJump-5215.git` for the nightly release
2. run the game with `pixeljump`

### Option 3.a: Running from source using `pip` (not reccomended)
1. Make sure you have `python3.10` installed. You can download and install it from https://www.python.org/downloads/
2. Clone the repo and `cd` into it
3. Create a python `venv`<sup>[1]</sup>
4. run `pip install pygame pygame-widgets` and `pip install -e .`
5. `cd src/pixeljump` and `python3 main.py`

### Option 3.b: Running from source using `poetry`
If you have [poetry](https://python-poetry.org/) installed, it will be easier since this project uses poetry
1. `cd pixeljump` and run `poetry install`
2. `cd src/pixeljump` and run `poetry shell`
3. Run the game with `python main.py`

[1] Create a `venv` by running `python3 -m venv venv`

### Configuring Game Settings
All the configurable settings are stored in the `settings/settings.json` file in the game folder.<br>
Since the current version of `PIXELJUMP` does not support in-game settings configuration yet, the only way to adjust the game settings is to edit the `settings.json` file.
#### Screen Resolution
The game is in `1920x1080` by default as it was the resolution we had in mind when designing the game but you can change it to your liking.<br>
The screen resolution of the game can be changed by adjusting the `screen_width` and `screen_height` keys in `settings.json`
#### FPS
It is not reccomended to change the FPS as it may cause some unwanted behaviours
#### Player velocity and gravity
Feel free to mess around with the velocity and gravity of the player :smile:


### Project Poster
![project_poster](https://drive.google.com/uc?export=view&id=1IXPpNm3-gM2gn9Cc_cCF63Dolu9mMFPT)
