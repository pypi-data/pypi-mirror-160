import click

from ..compatibility import COILED_VERSION
from .aws_setup import aws_setup
from .diagnostics import diagnostics
from .env import env
from .install import install
from .kubernetes import create_kubeconfig
from .login import login
from .upload import upload

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(COILED_VERSION, message="%(version)s")
def cli():
    """Coiled command line tool"""
    pass


cli.add_command(login)
cli.add_command(install)
cli.add_command(upload)
cli.add_command(env)
cli.add_command(create_kubeconfig)
cli.add_command(diagnostics)


@click.group(context_settings=CONTEXT_SETTINGS)
def setup():
    """Setup Coiled with cloud provider"""
    pass


cli.add_command(setup)
setup.add_command(aws_setup, "aws")
