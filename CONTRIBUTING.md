# <img src="https://i.imgur.com/hXiemtm.png" height=25> PyMine

## Contributing

_Want to help out? This is how! P.S. You get a shiny contributor role in the Discord server too!_

1. [Create a bug report, feature request, or other issue](https://github.com/py-mine/PyMine/issues), and assign yourself.
2. Fork the repository, or create a new branch.
3. Make your changes, with descriptive commit names.
4. [Create a pull request](https://github.com/py-mine/PyMine/pulls) with a detailed description of the issue resolved, link the issue you created, and request a reviewer.
5. One of the main devs will review it and request changes if needed!
6. _You should probably also [join our Discord server](https://discord.gg/dHjv7DJgb2), for news on the status and direction of the project_

Note: For vanilla server features (as PyMine plans to support all of them), don't create an issue without an attached pull request to add it.

### General Guidelines

- Use f-strings (`f"{thing}"`) instead of `.format()` where possible
- Use concatenation instead of f-strings where possible, as concatenation is faster
- Use `snake_case` for variables
- Constants should either be loaded from a config file or be in `UPPER_SNAKE_CASE`
- Lines shouldn't be longer than 127 characters.
- `black` formatting is required, however github actions takes care of it so you don't need to run it yourself..

### Imports

- Imports should be sorted by size descending
- Imports from `pymine/*` should be separated from the rest of the imports by a newline
- The tool [isort](https://pycqa.github.io/isort/) should do this for you, if installed

### Tools

#### VSCode

[@The456gamer](https://github.com/the456gamer) Has made a VSCode config to put in `.vscode/settings.json` [here](https://gist.github.com/the456gamer/cc3f6472391a8ae359be06547b07cdb2)
