#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for ipgetter2."""

import click
from .ipgetter2 import IPGetter, IPAddress


@click.command()
def main():
    """Console script for ipgetter2."""

    getter = IPGetter()
    click.echo(getter.get())


if __name__ == "__main__":
    main()
