from dataclasses import dataclass


@dataclass
class K8sVolumeClaimConfig:
    storage: str
