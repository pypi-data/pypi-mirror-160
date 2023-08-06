from pathlib import Path
from typing import List
import click
import os
import yaml

from dataclasses import asdict

from configurator.constants import DEFAULT_HOSTS_FILE_PATH
from configurator.hosts.host import Host


@click.group()
def host():
    """Host configuration activities"""


@host.command()
@click.argument("host-ip", type=click.STRING)
@click.argument("root-password", type=click.STRING)
@click.option(
    "-f",
    "--file",
    "file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_HOSTS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines hosts",
)
@click.pass_context
def add(
    ctx: click.Context,
    host_ip: str,
    root_password: str,
    file_path: Path,
):
    print(f"Adding host with IP {host_ip} and root password {root_password}")
    print(f"Using file path {file_path}")

    new_host = Host(host_ip, root_password)

    with open(file_path, "r") as hosts_file:
        hosts_dict = yaml.safe_load(hosts_file)
        if hosts_dict and hosts_dict["hosts"]:
            hosts_dict["hosts"].append(asdict(new_host))
        else:
            hosts_dict = {"hosts": [asdict(new_host)]}

    with open(file_path, "w") as hosts_file:
        yaml.safe_dump(hosts_dict, hosts_file)
        # TODO: check for duplicates


@host.command()
@click.argument("host-ip", type=click.STRING)
@click.option(
    "-f",
    "--file",
    "file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_HOSTS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines hosts",
)
@click.pass_context
def delete(
    ctx: click.Context,
    host_ip: str,
    file_path: Path,
):
    print(f"Deleting host with IP {host_ip}")
    print(f"Using file path {file_path}")

    with open(file_path, "r") as hosts_file:
        hosts_dict = yaml.safe_load(hosts_file)
        if not hosts_dict or not hosts_dict["hosts"]:
            print("Hosts file is empty. Nothing to delete")
        # hosts_dict["hosts"].remove(host_ip)
        new_hosts = []
        for host in hosts_dict["hosts"]:
            if Host(**host).ip_address != host_ip:
                new_hosts.append(host)

    with open(file_path, "w") as hosts_file:
        yaml.safe_dump({"hosts": new_hosts}, hosts_file)


@host.command(name="list")
@click.option(
    "-f",
    "--file",
    "file_path",
    type=Path,
    default=os.path.expandvars(DEFAULT_HOSTS_FILE_PATH),
    show_default=True,
    help="Path to the file which defines hosts",
)
@click.pass_context
def list_command(ctx: click.Context, file_path: Path):
    if not file_path.is_file():
        print("No hosts file found")
        return
    with open(file_path, "r") as hosts_file:
        hosts_dict = yaml.safe_load(hosts_file)
        if not hosts_dict or not hosts_dict["hosts"]:
            print("No hosts found")
            return

        host_list: List[Host] = []

        for host in hosts_dict["hosts"]:
            host_list.append(Host(**host))

        print("-----------------------------------")
        print(f"Hosts configured in {file_path}:")
        print(*host_list, sep="\n")  # TODO: maybe don't dump passwords onto STDOUT
        return host_list
