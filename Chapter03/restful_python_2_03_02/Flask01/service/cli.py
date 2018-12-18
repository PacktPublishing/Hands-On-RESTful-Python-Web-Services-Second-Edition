import click
from flask_cli import with_appcontext
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import init as _init
from flask_migrate import migrate as _migrate


@click.group()
def db():
    pass


@db.command()
@with_appcontext
def init(directory, multidb):
    """Creates a new migration repository."""
    _init()


@db.command()
@with_appcontext
def migrate(directory, message, sql, head, splice, branch_label, version_path,
            rev_id, x_arg):
    # Autogenerate a new revision file (Alias for 'revision --autogenerate')"""
    _migrate()
