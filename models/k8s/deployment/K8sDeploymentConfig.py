from dataclasses import dataclass


@dataclass
class K8sDeploymentConfig:
    memory: str
    cpu: str
    volume_claim: str
