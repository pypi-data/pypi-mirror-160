# BasketCase
Automates downloading images and videos from Instagram posts.

Known limitations:
- Stories and highlights are not supported yet.
- Although two-factor authentication is supported, only the `totp` method has been tested.

## Installation and usage
1. Install it from [PyPI](https://pypi.org/project/basketcase/).

```sh
pip install basketcase
```

> This will put the executable `basketcase` on your PATH.

2. Create a text file (e.g. `basketcase.txt`) and populate it with resource URLs.

```
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
https://www.instagram.com/p/<post_id>/
```

3. Pass the file as a positional argument. An interactive authentication procedure will follow.

```sh
basketcase ./basketcase.txt
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase_{timestamp}/`).

## User data
Cookies and other application data are kept in `~/.basketcase`.

## Development setup
1. `cd` to the project root and create a virtual environment in a directory named `venv`, which is conveniently ignored in version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

3. Install this package in editable mode.

```sh
pip install -e .
```

### Package build and upload
1. Update the requirements list.

```sh
pip freeze --exclude-editable > requirements.txt
```

2. Increment the version on `pyproject.toml`.
3. Build and publish the package

```sh
hatch build
hatch publish
```

4. Commit and push the changes (and the new version tag) to the git repository.
