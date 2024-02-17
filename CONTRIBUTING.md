## Development
This project is managed using [Poetry](https://poetry.eustace.io).


### Install poetry

```
pip install --upgrade pip
pip install poetry
```

### Setup virtualenvs

```
poetry config --local virtualenvs.in-project true
```

### Install dependencies

```
poetry install
```

### lint

```
poetry run ruff check .
poetry run ruff format . --check --diff
```

### test

```
poetry run pytest
```
