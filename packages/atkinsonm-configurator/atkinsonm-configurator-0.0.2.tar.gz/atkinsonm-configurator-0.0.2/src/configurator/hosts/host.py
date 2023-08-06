from dataclasses import dataclass


@dataclass
class Host:
    ip_address: str
    root_password: str
