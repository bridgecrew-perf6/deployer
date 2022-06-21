from dataclasses import dataclass


@dataclass
class K8sServiceConfig:
    node_port: str
