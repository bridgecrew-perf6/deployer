from dataclasses import dataclass
from datetime import datetime
from .K8sDeploymentStatus import K8sDeploymentStatus
from .K8sDeploymentConfig import K8sDeploymentConfig


@dataclass
class K8sDeployment:
    id: str
    status: K8sDeploymentStatus
    config: K8sDeploymentConfig
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()