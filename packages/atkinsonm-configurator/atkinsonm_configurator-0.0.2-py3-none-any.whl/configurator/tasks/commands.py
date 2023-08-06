from typing import List, Optional
import click
import os
from paramiko import AutoAddPolicy, SSHClient
from pathlib import Path
import yaml

from configurator.constants import (
    DEFAULT_HOSTS_FILE_PATH,
    DEFAULT_TASKS_FILE_PATH
)
from configurator.tasks.task import Task, TaskType, task_mapping
from configurator.hosts.commands import list_command as host_list_command
from configurator.hosts.host import Host
from configurator.tasks.task_steps import create_file, manage_package


@click.group()
def task():
    """Task activities"""


@task.command(name="list")  # list is a reserved word in Python
@click.option(
    "-f",
    "--file",
    "file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_TASKS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines tasks",
)
@click.pass_context
def list_command(ctx: click.Context, file_path: Path):
    if not file_path.is_file():
        print("No tasks file found")
        return
    with open(file_path, "r") as tasks_file:
        tasks_dict = yaml.safe_load(tasks_file)
        if not tasks_dict or not tasks_dict["tasks"]:
            print("No tasks found")
            return

        task_list: List[Task] = []

        for task in tasks_dict["tasks"]:
            task_list.append(convert_task_yaml_to_object(task))

        print("-----------------------------------")
        print(f"Tasks configured in {file_path}:")
        print(*task_list, sep="\n")
        return task_list


@task.command()
@click.option(
    "-h",
    "--hosts-file",
    "hosts_file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_HOSTS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines hosts",
)
@click.option(
    "-t",
    "--tasks-file",
    "tasks_file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_TASKS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines tasks",
)
@click.pass_context
def run(ctx: click.Context, hosts_file_path: Path, tasks_file_path: Path):
    tasks: List[Task] = ctx.invoke(list_command, file_path=tasks_file_path)
    hosts: List[Host] = ctx.invoke(host_list_command, file_path=hosts_file_path)

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())  # ignore unknown hosts

    for host in hosts:
        # TODO: support a username other than root
        print("-------------------------------------------")
        print(f"Starting tasks for host {host.ip_address}")
        client.connect(host.ip_address, username="root",
                       password=host.root_password)

        for task in tasks:
            if task.type == TaskType.file.name:
                create_file(task, client)

            elif task.type == TaskType.package.name:
                manage_package(task, client)

        client.close()
        print(f"Completed tasks for host {host.ip_address}")


def convert_task_yaml_to_object(task) -> Optional[Task]:
    valid_task_types = tuple(task_type.name for task_type in TaskType)

    try:
        task_obj = Task(**task)
        if task_obj.type not in valid_task_types:
            print(
                f"Task {task_obj.name} has invalid type '{task_obj.type}'. Valid values are {valid_task_types}")
        task_type_class = task_mapping.get(task_obj.type, Task)
        return task_type_class(**task)
    except (KeyError, TypeError):
        print(f"Invalid task definition for {task}")
        return None
