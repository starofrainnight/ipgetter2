#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for ipgetter2."""

import click
from .ipgetter1 import myip, IPgetter


@click.command()
def main():
    """Console script for ipgetter2."""

    click.echo(myip())


if __name__ == "__main__":
    main()
