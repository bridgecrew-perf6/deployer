from dataclasses import dataclass, field
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sResourceQuotaConfig import K8sResourceQuotaConfig


@dataclass
class K8sResourceQuota(JSONWizard):
    id: str
    config: K8sResourceQuotaConfig
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
