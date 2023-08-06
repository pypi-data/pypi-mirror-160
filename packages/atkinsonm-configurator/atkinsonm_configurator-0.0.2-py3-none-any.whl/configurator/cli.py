import click
import sys

from configurator.hosts import commands as host_commands
from configurator.tasks import commands as task_commands


@click.group()
# @click.version_option(package_name="atkinsonm-configurator")
@click.option(
    "--debug", type=click.BOOL, default=False, is_flag=True, help="Enable debug logging"
)
@click.pass_context
def cli(ctx: click.Context, debug: bool):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug


@cli.command()
def hello():
    print("Hello from Configurator!")


cli.add_command(host_commands.host)
cli.add_command(task_commands.task)

if __name__ == '__main__':
    args = sys.argv
    cli()
