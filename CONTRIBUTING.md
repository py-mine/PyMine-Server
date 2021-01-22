# <img src="https://i.imgur.com/hXiemtm.png" height=25> PyMine
## Contributing
*Want to help out? This is how!*

1. [Create a bug report, feature request, or other issue](https://github.com/py-mine/PyMine/issues), and assign yourself.
2. Fork the repository, or create a new branch.
3. Make your changes, with descriptive commit names.
4. [Create a pull request](https://github.com/py-mine/PyMine/pulls) with a detailed description of the issue resolved, link the issue you created, and request a reviewer.
5. One of the main devs will review it and request changes if needed!
6. *You should probably also [join our Discord server](discord.gg/dHjv7DJgb2), for news on the status and direction of the project*

### General Guidelines
* Use f-strings (`f"{thing}"`) instead of `.format()` where possible
* Use concatenation instead of f-strings where possible, as concatenation is faster
* Use `snake_case` for variables
* Constants should either be loaded from a config file or be in `UPPER_SNAKE_CASE`
* Lines shouldn't be longer than 127 characters.

### Imports
* Imports should be sorted by size descending
* Imports from `pymine/*` should be separated from the rest of the imports by a newline
