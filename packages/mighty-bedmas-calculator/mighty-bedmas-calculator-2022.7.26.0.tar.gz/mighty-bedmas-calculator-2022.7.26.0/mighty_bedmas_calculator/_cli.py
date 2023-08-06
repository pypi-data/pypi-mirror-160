"""Console script for Odyssey Settings."""
import json
import sys

from typing import Dict

import click

from mighty_bedmas_calculator.infix_evaluator import evaluate


@click.group()
def cli():
    pass


@cli.command()
@click.argument("expression")
def calculate(expression: str) -> str:
    """List configured settings, optionally filtering by search term."""
    click.echo(evaluate(expression))


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
