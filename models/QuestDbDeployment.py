from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from dataclass_wizard import JSONWizard

from models.k8s.K8sMetadata import K8sMetadata
from .QuestDbDeploymentStatus import QuestDbDeploymentStatus


@dataclass
class QuestDbDeployment(JSONWizard):
    status_log: list[QuestDbDeploymentStatus] = field(
        default_factory=lambda: [QuestDbDeploymentStatus.CREATION_SCHEDULED])
    id: UUID = field(default_factory=lambda: uuid4())
    status: QuestDbDeploymentStatus = QuestDbDeploymentStatus.CREATION_SCHEDULED
    k8s_metadata: K8sMetadata = field(default_factory=lambda: K8sMetadata())
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
