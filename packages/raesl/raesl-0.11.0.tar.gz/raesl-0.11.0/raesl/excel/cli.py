"""ESL to Excel Command Line Interface."""

import sys
from typing import Iterable, Tuple

import click
import raesl.excel
import raesl.excel.defaults
from raesl import logger


@click.command("excel")
@click.argument(
    "paths", nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=True)
)
@click.option(
    "--output",
    "-o",
    default=raesl.excel.defaults.OUTPUT,
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Output file to write to.",
    show_default=True,
)
@click.option(
    "--scope",
    "-s",
    default=[("world", -1)],
    type=(str, int),
    multiple=True,
    help=(
        "Scopes in the component hierarchy. "
        "Expects component instance paths and the relative depth you want to include. "
        "A depth of -1 includes everything below that component."
    ),
    show_default=True,
)
def excel(paths: Iterable[str], output: str, scope: Iterable[Tuple[str, int]]):
    """Convert ESL files and/or directories to an Excel workbook."""
    logger.info("This is the Ratio ESL Excel command line utility.")
    logger.info(f"Populating '{output}'...")
    try:
        raesl.excel.convert(
            *paths,
            output=output,
            scopes={s[0]: s[1] if s[1] >= 0 else None for s in scope},
        )
        logger.info("Excel generation done!")
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    excel()
