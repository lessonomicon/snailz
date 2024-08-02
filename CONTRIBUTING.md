# Contributing

Contributions are very welcome.
Please file issues or submit pull requests in our GitHub repository.
All contributors will be acknowledged,
but must abide by our Code of Conduct.

## Site Structure

-   `README.md`: overview
-   `LICENSE.md`: content license
-   `CODE_OF_CONDUCT.md`: code of conduct
-   `CONTRIBUTING.md`: this contributors' guide
-   `pyproject.toml`: Python package description
-   `Makefile`: repeatable commands
-   `src/snailz/`: Python source
    -   `src/snailz/params/`: sample data synthesis parameters
-   `data/`: sample synthesized data
-   `img/`: images

## Build and Release

-   `pip install build twine`
-   `python -m build`
-   `twine upload --verbose -u __token__ -p pypi-your-access-token dist/*`
