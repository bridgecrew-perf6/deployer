from dataclasses import dataclass


@dataclass
class K8sResourceQuotaConfig:
    memory: str
    cpu: str
