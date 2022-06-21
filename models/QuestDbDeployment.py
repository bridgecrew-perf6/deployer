from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime
from .QuestDbDeploymentStatus import QuestDbDeploymentStatus
from models.k8s.K8sMetadata import K8sMetadata


@dataclass
class QuestDbDeployment:
    status_log: list[QuestDbDeploymentStatus] = field(default_factory=lambda: [QuestDbDeploymentStatus.CREATION_SCHEDULED])
    id: UUID = uuid4()
    status: QuestDbDeploymentStatus = QuestDbDeploymentStatus.CREATION_SCHEDULED
    k8s_metadata: K8sMetadata = K8sMetadata()
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
