from gettext import install
from paramiko import SSHClient

from configurator.tasks.task import FileTask, PackageTask


def create_file(task: FileTask, client: SSHClient):
    # TODO: add some safety
    print(f"Creating file {task.path}...")
    client.exec_command(f"echo '{task.contents}' > {task.path}")
    client.exec_command(f"chown {task.owner}:{task.group} {task.path}")
    client.exec_command(f"chmod {task.mode} {task.path}")
    if task.restart_service:
        client.exec_command(f"service {task.restart_service} restart")


def manage_package(task: PackageTask, client: SSHClient):
    if task.install:
        install_package(task, client)
    else:
        uninstall_package(task, client)
    if task.restart_service:
        client.exec_command(f"service {task.restart_service} restart")


def install_package(task: PackageTask, client: SSHClient):
    print(f"Installing {task.package_name}...")
    stdin, stdout, stderr = client.exec_command(
        f'apt install {task.package_name} -y')
    # print(stdout)
    # print(stderr)
    stdout.channel.set_combine_stderr(True)
    # need this so we can be sure that the operation completes and dpkg lock releases
    output = stdout.readlines()
    # print (output)


def uninstall_package(task: PackageTask, client: SSHClient):
    print(f"Removing {task.package_name}...")
    stdin, stdout, stderr = client.exec_command(
        f'apt remove {task.package_name} -y')
    # print(stdout)
    # print(stderr)
    stdout.channel.set_combine_stderr(True)
    # need this so we can be sure that the operation completes and dpkg lock releases
    output = stdout.readlines()
    # print (output)
    stdin, stdout, stderr = client.exec_command(
        f'apt autoremove -y')  # autoremove no longer used packages
    # print(stdout)
    # print(stderr)
    stdout.channel.set_combine_stderr(True)
    # need this so we can be sure that the operation completes and dpkg lock releases
    output = stdout.readlines()
    # print (output)
