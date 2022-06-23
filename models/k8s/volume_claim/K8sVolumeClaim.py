from dataclasses import dataclass, field
from datetime import datetime
from dataclass_wizard import JSONWizard

from .K8sVolumeClaimConfig import K8sVolumeClaimConfig


@dataclass
class K8sVolumeClaim(JSONWizard):
    id: str
    config: K8sVolumeClaimConfig
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
