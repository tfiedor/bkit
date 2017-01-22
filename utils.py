import click

__author__ = 'Tomas Fiedor'


def abort(message):
    click.echo("Aborting {}".format(message))
    exit(0)


def log(message):
    click.echo('[bkit log] %s' % message)


def warn(message):
    click.echo('[bkit warn] %s' % message)


def error(message):
    click.echo('[bkit error] %s' % message)
    exit(1)
