# PyMine
## Contributing
*Want to help out? This is how!*

1. [Create a bug report, feature request, or other issue](https://github.com/py-mine/PyMine/issues), and assign yourself.
2. Fork the repository, or create a new branch.
3. Make your changes, with descriptive commit names. Remember to follow the [style guide](#style-guide)!
4. [Create a pull request](https://github.com/py-mine/PyMine/pulls) with a detailed description of the issue resolved, link the issue you created, and request a reviewer.
5. One of the main devs will review it and request changes if needed!

## Style Guide
* Use `'string'` not `"string"`
* Use f-strings (`f'{thing}'`) instead of `.format()` where possible
* After indentation changes there should be a new line
* There should be two new lines before a class or function header unless it's indented
* Unless there's a good reason, lines shouldn't be longer than 100 characters
* Use `snake_case` for variables
* Constants should either be loaded from a config file or be in `UPPER_SNAKE_CASE`
* Docstrings should be present for classes and functions with a newline after them
* Docstrings that are too long should not start on the same line as `"""`
* Docstrings that are small enough should look like `"""Information"""`
* Imports should be sorted by size descending
* Imports from `src/*` should be seperated from the rest of the imports by a newline
