from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sServiceConfig import K8sServiceConfig


@dataclass
class K8sService(JSONWizard):
    id: str
    config: K8sServiceConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
