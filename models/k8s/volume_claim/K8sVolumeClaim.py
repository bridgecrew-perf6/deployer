from dataclasses import dataclass
from datetime import datetime

from .K8sVolumeClaimConfig import K8sVolumeClaimConfig


@dataclass
class K8sVolumeClaim:
    id: str
    config: K8sVolumeClaimConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
