from uuid import UUID

from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from repositories import QuestDbDeploymentRepo
from services import CreationService, DeletionService


async def create() -> QuestDbDeployment:
    scheduled_deployment = await QuestDbDeploymentRepo.create()
    pending_deployment = await CreationService.create(scheduled_deployment)
    return pending_deployment.to_json()


async def delete(deployment_id: UUID) -> QuestDbDeployment:
    scheduled_deletion_deployment = await QuestDbDeploymentRepo.update_status(deployment_id,
                                                                              QuestDbDeploymentStatus.DELETION_SCHEDULED)
    pending_deletion_deployment = await DeletionService.delete(scheduled_deletion_deployment)
    return pending_deletion_deployment.to_json()


async def get(deployment_id: UUID) -> QuestDbDeployment:
    return (await QuestDbDeploymentRepo.get(deployment_id)).to_json()


async def get_status(deployment_id: UUID):
    deployment = (await QuestDbDeploymentRepo.get(deployment_id))
    return { "status": deployment.status }
