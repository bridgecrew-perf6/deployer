from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sResourceQuotaConfig import K8sResourceQuotaConfig


@dataclass
class K8sResourceQuota(JSONWizard):
    id: str
    config: K8sResourceQuotaConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
