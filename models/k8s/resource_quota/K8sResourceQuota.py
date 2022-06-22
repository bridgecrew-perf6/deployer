from dataclasses import dataclass
from datetime import datetime

from .K8sResourceQuotaConfig import K8sResourceQuotaConfig


@dataclass
class K8sResourceQuota:
    id: str
    config: K8sResourceQuotaConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
