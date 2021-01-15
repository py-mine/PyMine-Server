# <img src="https://cdn.discordapp.com/emojis/783838348695437353.gif?v=1" height=45>PyMine
## Contributing
*Want to help out? This is how!*

1. [Create a bug report, feature request, or other issue](https://github.com/py-mine/PyMine/issues), and assign yourself.
2. Fork the repository, or create a new branch.
3. Make your changes, with descriptive commit names. Remember to follow the [style guide](#style-guide)!
4. [Create a pull request](https://github.com/py-mine/PyMine/pulls) with a detailed description of the issue resolved, link the issue you created, and request a reviewer.
5. One of the main devs will review it and request changes if needed!
6. *You should probably also [join our Discord server](discord.gg/dHjv7DJgb2), for news on the status and direction of the project*

## Style Guide
### General Guidelines
* Use `'string'` not `"string"`
* Use f-strings (`f'{thing}'`) instead of `.format()` where possible
* Use concatenation for uncomplicated things instead of f-strings, as concatenation is faster
* If indentation changes such so there's less indentation afterwards, there should be a newline following sed change.
* Unless there's a good reason, lines shouldn't be longer than 100 characters
* Use `snake_case` for variables
* Constants should either be loaded from a config file or be in `UPPER_SNAKE_CASE`
* Standalone tuples should always be incased in () and have an extra comma at the end. Example: `my_tup = (val1, val2,)`
* Lines shouldn't be longer than 127 characters.

### Classes
* There should be two new lines before the start of a class unless it's indented
* Must have descriptive docstring
* Must have typehints for `__init__` arguments

### Functions/Methods
* There should be two new lines before the start of a function unless it's indented
* Must have a semi-descriptive docstring
* Must have typehints for arguments and return type annotations for returns
* If a method's return type is the method's class, do `from __future__ import annotations` to fix NameErrors

### Docstrings
* Docstrings should be present for files, classes, and functions with a newline after them
* Docstrings that are small enough should look like `"""Information"""`

### Imports
* Imports should be sorted by size descending
* Imports from `pymine/*` should be separated from the rest of the imports by a newline
