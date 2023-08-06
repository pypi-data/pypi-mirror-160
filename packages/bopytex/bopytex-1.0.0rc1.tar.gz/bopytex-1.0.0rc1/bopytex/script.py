#!/usr/bin/env python
# encoding: utf-8


import logging

import click

from bopytex.service import main

formatter = logging.Formatter("%(name)s :: %(levelname)s :: %(message)s")
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
steam_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)


@click.command()
@click.argument(
    "template",
    type=click.Path(exists=True),
    nargs=1,
)
@click.option(
    "-w",
    "--working-dir",
    default=".",
    type=click.Path(exists=True),
)
@click.option(
    "-s",
    "--students-csv",
    type=str,
    default="",
    help="CSV containing list of students names",
)
@click.option(
    "-n",
    "--no-compile",
    is_flag=True,
    default=False,
    help="Do not compile source code",
)
@click.option(
    "-d",
    "--dirty",
    is_flag=True,
    default=False,
    help="Do not clean after compilation",
)
@click.option(
    "-q",
    "--quantity_subjects",
    type=int,
    default=1,
    help="The quantity of subjects to make",
)
@click.option(
    "-j",
    "--no-join",
    is_flag=True,
    default=False,
    help="Do not join pdfs to a single pdf and remove individuals",
)
@click.option(
    "-O",
    "--only-corr",
    is_flag=True,
    default=False,
    help="Activate correction and compile only from existing subjects",
)
@click.option(
    "-C",
    "--corr",
    is_flag=True,
    default=False,
    help="Create and compile correction while making subjects",
)
@click.option(
    "-c",
    "--configfile",
    type=str,
    default="bopyptex_config.py",
    help="Config file path",
)
def new(**options):
    for message in main(**options):
        try:
            assert message.status == 0
        except AssertionError:
            logger.warning(message)
            break
        else:
            logger.info(message.out)


if __name__ == "__main__":
    new()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del
