from models.QuestDbDeployment import QuestDbDeployment
from uuid import UUID


async def create() -> QuestDbDeployment:
    raise Exception("Not implemented")


async def delete(deployment_id: UUID) -> QuestDbDeployment:
    raise Exception("Not implemented")


async def get(deployment_id: UUID) -> QuestDbDeployment:
    raise Exception("Not implemented")
