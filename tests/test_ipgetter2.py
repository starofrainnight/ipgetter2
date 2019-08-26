#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ipgetter2` package."""

from click.testing import CliRunner

from ipgetter2.__main__ import main


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()

    result = runner.invoke(main, ["show-servers"])
    assert result.exit_code == 0

    help_result = runner.invoke(main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_backport_random():
    """Test the backport randome for python 3.5"""

    import random
    from ipgetter2.compatible import backport_random_choices

    population = range(1, 6)
    choices = backport_random_choices(random._inst, population)
    assert len(set(choices) & set(population)) > 0
