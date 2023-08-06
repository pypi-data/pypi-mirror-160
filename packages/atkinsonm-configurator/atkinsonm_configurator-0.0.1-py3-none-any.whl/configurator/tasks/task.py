from dataclasses import dataclass
from enum import auto, Enum
from typing import Optional
from dataclasses_json import dataclass_json, Undefined


class TaskType(Enum):
    file = auto()
    package = auto()


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Task:
    name: str
    type: TaskType

# This doesn't work well with dataclasses in 3.8, but in 3.10 the kw_only argument may help
# @dataclass_json(undefined=Undefined.EXCLUDE)
# @dataclass(kw_only=True)
# class RestartServiceTask(Task):
#     restart_service: Optional[str] = None


@dataclass
class FileTask(Task):
    """Creates a file with the specified options. DESTRUCTIVE to existing files"""
    path: str
    contents: str
    owner: str
    group: str
    mode: int  # TODO: verify this is a valid permission
    restart_service: Optional[str] = None


@dataclass
class PackageTask(Task):
    """Installing and removing packages (Debian support only)"""  # TODO: support other package managers
    package_name: str
    install: bool
    restart_service: Optional[str] = None


task_mapping = {
    "file": FileTask,
    "package": PackageTask,
}
