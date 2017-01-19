import atexit
import click
import os
import core
import utils
import config

__author__ = 'Tomas Fiedor'


@click.group()
@click.option('--discover', '-d', default=False,
              help='discovers .bkits inside the whole filesystem')
def cli(discover):
    """bkit is a simple backup control system

    TODO: Maybe the registering should be confirmed?
    """
    if discover:
        for bkit_dir in core.get_existing_bkit_dirs():
            if not core.is_registered(bkit_dir):
                core.register_bkit(bkit_dir)
    click.echo('Hello world!')
    atexit.register(config.save_config)


@cli.command(short_help='Initializes bkit repository')
@click.argument('dst', required=False, default=os.getcwd())
@click.option('--verify', '-c', default=False,
              help='verifies if there exists bkit directory in the system already')
def init(dst, verify):
    """Inits the bkit repository"""
    utils.log("Called bkit.init()")

    # if there exists bkit directories, ask for confirmation
    if verify and len(core.get_registered_bkits()):
        utils.log('Found following .bkit directories')
        click.confirm('Continue?')

    if not os.path.isdir(dst):
        utils.error("'%s' is not a valid directory" % dst)

    core.initialize_bkit_dir(os.path.join(dst, '.bkit'))


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
