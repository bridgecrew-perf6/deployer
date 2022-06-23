from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sDeploymentConfig import K8sDeploymentConfig
from .K8sDeploymentStatus import K8sDeploymentStatus


@dataclass
class K8sDeployment(JSONWizard):
    id: str
    status: K8sDeploymentStatus
    config: K8sDeploymentConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
