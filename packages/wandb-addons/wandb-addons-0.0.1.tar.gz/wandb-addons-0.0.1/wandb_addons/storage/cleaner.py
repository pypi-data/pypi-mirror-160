from __future__ import annotations

import os
import subprocess
from typing import Optional, Union

import rich
import wandb
from inputidy import prompt_input
from wandb.apis.public import Runs

# Project should be specified by <entity/project-name>


def find_runs(user: str, project: str, api: Optional[wandb.Api] = None) -> Runs:
    if api is None:
        api = wandb.Api()

    runs = api.runs(f"{user}/{project}")
    return runs


def find_multiple_project_runs(
    user: Union[str, list[str]], projects: list[str], api: Optional[wandb.Api] = None
) -> dict[str, list[str]]:
    if api is None:
        api = wandb.Api()

    all_runs = {}
    for project in projects:
        try:
            runs = find_runs(user, project, api=api)
            name_list = []
            for run in runs:
                name_list.append(run.path[-1])
            all_runs[project] = name_list
        except ValueError:
            continue
    return all_runs


def find_multiple_project_runs_local(local_dir: str) -> dict[str, list[str]]:
    all_runs = {}
    local_projects = os.listdir(local_dir)
    for project in local_projects:
        if not os.path.isdir(os.path.join(local_dir, project)):
            continue
        all_runs[project] = os.listdir(os.path.join(local_dir, project))

    return all_runs


def run_information(server_runs, local_runs, print_table=False) -> dict[str, list[str]]:
    from rich.console import Console

    console = Console()
    table = rich.table.Table(title="Weights & Biases Runs")
    table.add_column("Project", style="red", no_wrap=True)
    table.add_column("# of server runs", style="cyan", no_wrap=True)
    table.add_column("# of local runs", style="magenta")

    removing = {}
    for key, value in local_runs.items():
        if key in server_runs:
            table.add_row(key, str(len(server_runs[key])), str(len(value)))
            removing[key] = [run for run in value if run not in server_runs[key]]
        else:
            table.add_row(key, str(0), str(len(value)))
            removing[key] = value

    if print_table:
        console.print(table)
    return removing


def clean_removed_runs(
    user: str, local_dir: str, password: Optional[str] = None, execute: bool = False
) -> None:
    local_dir = os.path.join(local_dir, "minio", "local-files", user)
    rich.print(f"List removed runs in {local_dir} for {user}. (execute = {execute})")
    api = wandb.Api()
    local_projects = os.listdir(local_dir)

    all_server_runs = find_multiple_project_runs(user, local_projects, api=api)
    all_local_runs = find_multiple_project_runs_local(local_dir)

    removing = run_information(all_server_runs, all_local_runs, print_table=True)
    if password is None:
        exit()

    num_removed = sum([len(v) for _, v in removing.items()])
    msg = f"Found {num_removed} removed runs, delete all removed local runs? (y/n)"
    if not prompt_input(msg, str) == "y":
        exit

    cmd_pssw = subprocess.Popen(["echo", password], stdout=subprocess.PIPE)
    for project, runs in removing.items():
        for run in runs:
            command = ["rm", "-r", os.path.join(local_dir, project, run)]
            if execute:
                _ = subprocess.Popen(
                    ["sudo", "-S"] + command, stdin=cmd_pssw.stdout, stdout=subprocess.PIPE
                )
            else:
                print(f" ".join(command))
