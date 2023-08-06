from __future__ import annotations

import click as _click
import rich
from inputidy import prompt_input


class RunGroup(_click.Group):
    def get_command(self, ctx, cmd_name):
        rv = _click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        return None


@_click.command(cls=RunGroup, invoke_without_command=True)
@_click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        _click.echo(ctx.get_help())


@cli.command("sort_local", help="Sort removed runs in local directory.")
@_click.option("-u", "--target_user", default=None, help="The user of W&B to clean runs for.")
@_click.option(
    "-d",
    "--local_dir",
    default=None,
    help="The local directory to clean runs in. Please try to run `docker inspect -f '{{ .Mounts }}' wandb-local`",
)
def sort_local(target_user, local_dir) -> None:
    from wandb_addons.storage import clean_removed_runs

    if target_user is None:
        target_user = prompt_input("Enter target user: ", str)
    if local_dir is None:
        local_dir = prompt_input("Enter local directory: ", str)

    clean_removed_runs(target_user, local_dir)


@cli.command("clean_local", help="clean removed runs in local directory (superuser required).")
@_click.option("-u", "--target_user", default=None, help="The user of W&B to clean runs for.")
@_click.option(
    "-d",
    "--local_dir",
    default=None,
    help="The local directory to clean runs in. Please try to run `docker inspect -f '{{ .Mounts }}' wandb-local`",
)
@_click.option(
    "-p", "--password", default=None, help="Superuser's Password of local server running W&B."
)
@_click.option("-e", "--execute", default=False, is_flag=True, help="execute the deletion")
def clean_local(target_user, local_dir, password, execute) -> None:
    from wandb_addons.storage import clean_removed_runs

    if target_user is None:
        target_user = prompt_input("Enter target user: ", str)
    if local_dir is None:
        local_dir = prompt_input("Enter local directory: ", str)
    if password is None:
        password = prompt_input("Enter password: ", str)

    clean_removed_runs(target_user, local_dir, password, execute)
    if not execute:
        rich.print("Deleteion is not executed, run with '-e' for actual execution.")
