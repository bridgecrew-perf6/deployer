from dataclasses import dataclass


@dataclass
class K8sDeploymentConfig:
    memory: str
    cpu: str
    storage: str
