# <img src="https://cdn.discordapp.com/emojis/783838348695437353.gif?v=1" height=45> PyMine [![discord](https://img.shields.io/discord/789623993547227147.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/eeyEcwR9EM) ![quality](https://www.codefactor.io/repository/github/py-mine/pymine/badge) ![code size](https://img.shields.io/github/languages/code-size/py-mine/PyMine?color=0FAE6E) ![issues](https://img.shields.io/github/issues/py-mine/PyMine) ![build status](https://img.shields.io/github/workflow/status/py-mine/PyMine/Python%20application?event=push)
*PyMine - The fastest, easiest to use, Python-based Minecraft Server!*


## Features
*Note: This list is not always up to date, and doesn't contain all the features that PyMine offers*
<!--☐☒-->
- **☐ Joinable** - *the login process is complete, but users can not yet join the world*
- **☐ Packet Models** - *missing some clientbound packets*
- **☒ Status + Login Logic** - *completed*
- **☐ Play Logic** - *not started yet*
- **☐ World Generation** - *not started yet*
- **☐ Entities/Entity AI** - *not started yet*
- **☒ Plugin API** - *completed, but more will be added as the development continues*


## Installation / Usage
- For now, PyMine will not be packaged as a binary, you'll have to install everything yourself.
### Installing from source
- First, clone the repository `git clone https://github.com/py-mine/PyMine.git` and move into that directory (`cd PyMine`)
- Next, install the required Python packages via pip (`pip install -r requirements.txt`)
- To run the server, you should run `server.py` from the root directory, like `python3 pymine/server.py`
- It is recommended you do not use regular Python, but [PyPy3](https://www.pypy.org/)


## Contributing
- Please read [CONTRIBUTING.md](https://github.com/py-mine/PyMine/blob/main/CONTRIBUTING.md)


## API/Plugin Examples
- [example-plugin](https://github.com/py-mine/example-plugin) - *the official example plugin*
- [FAP](https://github.com/py-mine/FAP) - *a plugin that auto-updates/manages other plugins*
