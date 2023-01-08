# Team international test

## Instalation

### Dependencies
- [python](https://www.python.org/downloads/)
- [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

### Set up and run
1. Download and install python
2. Download and install poetry
3. Run the poetry command to set up the enviroment
    ```
    poetry install
    ```
4. Run the unit test and validate the metrics
    ```
    poetry run pytest -vv --cov-report term-missing  --cov=technical_test tests
    ```