import click

__author__ = 'Tomas Fiedor'


@click.command()
def cli():
    """bkit is a simple backup control system"""
    click.echo('Hello world!')

if __name__ == "__main__":
    cli()
