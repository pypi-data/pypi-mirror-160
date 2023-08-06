# The Might BEDMAS Calculator v2022.7.26.0
A package to calculate infix expressions following BEDMAS.

## Features

This will calculate an expression following thr BEDMAS order of operations and the following operators are supported:

* Add +
* Subtract -
* Multiply *
* Divide /
* Power of ^
* Brakcets ()

## Usage via the command line

    ❯ pip install git+ssh://git@github.com/jdboisvert/mightly-bedmas-calculator

    ❯ mighty-bedmas-calculator calculate "2+2"
    4

    ❯ mighty-bedmas-calculator calculate "2-3"
    -1

    ❯ mighty-bedmas-calculator calculate "(2+3)^4"
    625


## Development

### Getting started

    pip install -r requirements_dev.txt

    # set up pre-commit hooks
    pre-commit install

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.

### Testing

[pytest](https://docs.pytest.org/en/6.2.x/) is used for testing.

    # just the unit tests against your current python version
    pytest

    # just the unit tests with a matching prefix
    pytest -k test_some_function
