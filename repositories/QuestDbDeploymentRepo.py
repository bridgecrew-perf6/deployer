from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from models.k8s.K8sMetadata import K8sMetadata
from uuid import UUID


async def create() -> QuestDbDeployment:
    raise Exception("Not implemented")


async def get(deployment_id: UUID) -> QuestDbDeployment:
    raise Exception("Not implemented")


async def find_by_status(status: QuestDbDeploymentStatus) -> list[QuestDbDeployment]:
    raise Exception("Not implemented")


async def update_status(deployment_id: UUID, status: QuestDbDeploymentStatus) -> QuestDbDeployment:
    raise Exception("Not implemented")


async def update_metadata(deployment_id: UUID, metadata: K8sMetadata) -> QuestDbDeployment:
    raise Exception("Not implemented")
