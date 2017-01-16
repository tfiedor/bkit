import click

__author__ = 'Tomas Fiedor'


@click.group()
def cli():
    """bkit is a simple backup control system"""
    click.echo('Hello world!')


@cli.command(short_help='Initializes bkit repository')
def init():
    """Inits the bkit repository"""
    click.echo('bkit init run')


@cli.group(short_help='Makes new incremental or standalone backup pack')
def make():
    """Makes new incremental or standalone backup pack"""
    click.echo('bkit make run')


@make.command(short_help='Makes new standalone backup pack')
def new():
    """Makes new standalone backup pack"""
    click.echo('bkit make new')


@make.command(short_help='Makes new delta backup pack')
def delta():
    """Makes new delta backup pack"""
    click.echo('bkit make delta')


@cli.command(short_help='Applies backup pack to given directory')
def apply():
    """Applies backup pack to given directory"""
    click.echo('bkit apply')


@cli.command(short_help='Prints log of tracked backup files')
def log():
    """Prints log of tracked backup on the file system"""
    click.echo('bkit log')


@cli.command(short_help='Print status of the initialized bkit')
def status():
    """Prints status of the initialized bkit"""
    click.echo('bkit status')


if __name__ == "__main__":
    cli()
