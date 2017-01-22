import atexit
import click
import os
import core
import utils
import config

__author__ = 'Tomas Fiedor'

pass_bkit = click.make_pass_decorator(core.BkitRepository, ensure=True)

@click.group()
@click.option('--discover', '-d', default=False, is_flag=True,
              help='discovers .bkits inside the whole filesystem')
@click.option('--bkit', '-b', nargs=1, default=None,
              help='specification of tag or path name to valid bkit')
@click.pass_context
def cli(ctx, discover, bkit):
    """bkit is a simple backup control system"""
    if discover:
        if click.confirm('bkit discovery may take lot of time. Are you sure?'):
            utils.log("Discovering bkits in filesystem")
            for bkit_dir in core.get_existing_bkit_dirs():
                if not core.is_registered(bkit_dir):
                    core.register_bkit(bkit_dir)
        else:
            utils.abort(".")

    # if the dst param is supplied we construct the directory
    if bkit is not None:
        try:
            ctx.obj = core.create_bkit_from_id(bkit)
        except utils.BkitFailureException:
            utils.abort("passed unknown tag or directory.")

    # Save registering of the new config
    atexit.register(config.save_config)


@cli.command(short_help='Initializes bkit repository')
@click.argument('dst', required=False, default=os.getcwd())
@click.option('--verify', '-c', default=False,
              help='verifies if there exists bkit directory in the system already')
def init(dst, verify):
    """Inits the bkit repository"""
    utils.log("Called bkit.init()")

    # if there exists bkit directories, ask for confirmation
    bkits = core.get_registered_bkits()
    if verify and len(bkits):
        utils.log('Found following .bkit directories')
        for bkit in bkits:
            assert bkit is not None
            utils.log(" -> {}".format(bkit))
        if not click.confirm('Continue?'):
            utils.abort("initialization of directory '{}'.".format(dst))

    if not os.path.isdir(dst):
        utils.error("'{}' is not a valid directory".format(dst))

    core.initialize_bkit_dir(os.path.join(dst, '.bkit'))


@cli.group(short_help='Makes new incremental or standalone backup pack')
@pass_bkit
def make(bkit):
    """Makes new incremental or standalone backup pack"""
    pass


@make.command(short_help='Makes new standalone backup pack')
@pass_bkit
def new(bkit):
    """Makes new standalone backup pack"""
    click.echo('bkit make new at {}'.format(bkit))


@make.command(short_help='Makes new delta backup pack')
@pass_bkit
def delta(repo):
    """Makes new delta backup pack"""
    click.echo('bkit make delta at {}'.format(repo))


@cli.command(short_help='Applies backup pack to given directory')
@pass_bkit
def apply(bkit):
    """Applies backup pack to given directory"""
    click.echo('bkit apply at {}'.format(bkit))


@cli.command(short_help='Prints log of tracked backup files')
@pass_bkit
def log(bkit):
    """Prints log of tracked backup on the file system"""
    click.echo('bkit log of {}'.format(bkit))


@cli.command(short_help='Print status of the initialized bkit')
@pass_bkit
def status(bkit):
    """Prints status of the initialized bkit"""
    click.echo('bkit status of {}'.format(bkit))


if __name__ == "__main__":
    cli()
