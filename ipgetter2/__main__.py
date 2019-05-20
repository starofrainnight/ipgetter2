#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for ipgetter2."""

import click
from .ipgetter2 import IPGetter, IPAddress, DEFAULT_URLS


@click.group()
def main():
    """Simple script for get/test external IP"""
    pass


@main.command()
def get():
    """Get the external IP randomly from default servers"""

    getter = IPGetter()
    click.echo(getter.get())


@main.command()
def test():
    """Test default servers"""

    getter = IPGetter()
    contexts = []
    failed = []
    counted = dict()

    i = 0
    click.echo("%s servers needs to be tested : " % len(DEFAULT_URLS))
    for url in DEFAULT_URLS:
        i += 1

        try:
            click.echo("[%s/%s] Testing : %s" % (i, len(DEFAULT_URLS), url))
            address = getter.get_from(url)
            contexts.append((address, url))

            if address in counted:
                counted[address] += 1
            else:
                counted[address] = 1
        except Exception as e:
            click.echo(
                "Test failed on %s, with exception : %s" % (url, e), err=True
            )

            failed.append(url)

    click.echo("Total urls : %s" % (len(DEFAULT_URLS), DEFAULT_URLS))
    click.echo("Failed %s urls : %s" % (len(failed), failed))

    click.echo(counted)
    click.echo(max(counted.items(), lambda item: item[1]))


@main.command()
def show_servers():
    """Display default servers' urls"""

    i = 0
    for url in DEFAULT_URLS:
        click.echo("%s: %s" % (i, url))
        i += 1


if __name__ == "__main__":
    main()
