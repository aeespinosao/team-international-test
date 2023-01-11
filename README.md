# Team international test

## Context
Create a program that computes some basic statistics on a collection of small positive integers. You can assume all values will be less than 1,000.

## Restriction
- You cannot import a library that solves it instantly.
- The methods add(), less(), greater(), and between() should have constant time O(1).
- The method build_stats() can be at most linear O(n).
- Apply the best practices you know.
- Share a public repo with your project.

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