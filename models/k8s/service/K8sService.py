from dataclasses import dataclass, field
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sServiceConfig import K8sServiceConfig


@dataclass
class K8sService(JSONWizard):
    id: str
    config: K8sServiceConfig
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
