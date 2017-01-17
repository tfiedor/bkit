import click

__author__ = 'Tomas Fiedor'


def log(message):
    click.echo('[bkit log] %s' % message)


def warn(message):
    click.echo('[bkit warn] %s' % message)


def error(message):
    click.echo('[bkit error] %s' % message)
    exit(0)
