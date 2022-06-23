from dataclasses import dataclass, field
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sDeploymentConfig import K8sDeploymentConfig
from .K8sDeploymentStatus import K8sDeploymentStatus


@dataclass
class K8sDeployment(JSONWizard):
    id: str
    status: K8sDeploymentStatus
    config: K8sDeploymentConfig
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
