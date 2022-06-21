from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus


async def schedule_status_updates():
    raise Exception("Not implemented")


async def update_status(deployment: QuestDbDeployment):
    raise Exception("Not implemented")


async def validate_next_status(deployment: QuestDbDeployment, status: QuestDbDeploymentStatus):
    raise Exception("Not implemented")


async def recalculate_running_status(deployment: QuestDbDeployment) -> QuestDbDeploymentStatus:
    raise Exception("Not implemented")


async def recalculate_deletion_status(deployment: QuestDbDeployment) -> QuestDbDeploymentStatus:
    raise Exception("Not implemented")
