from dataclasses import dataclass


@dataclass
class ConnectionData:
    host: str
    port: int
    login: str
    password: str
    virtualhost: str
