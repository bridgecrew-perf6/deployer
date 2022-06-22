from dataclasses import replace
from typing import Callable
from uuid import UUID

from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from models.k8s.K8sMetadata import K8sMetadata

deployments: dict[UUID, QuestDbDeployment] = {}


async def create() -> QuestDbDeployment:
    deployment = QuestDbDeployment()
    deployments[deployment.id] = deployment
    return deployment


async def get(deployment_id: UUID) -> QuestDbDeployment:
    deployment = deployments[deployment_id]
    if deployment is None: raise Exception(f"Deployment with id {deployment_id} not found")

    return deployment


async def find_by_status(status: QuestDbDeploymentStatus) -> list[QuestDbDeployment]:
    values: list[QuestDbDeployment] = list(deployments.values())
    status_filter: Callable[[QuestDbDeployment], bool] = lambda deployment: deployment.status == status

    return list(filter(status_filter, values))


async def update_status(deployment_id: UUID, status: QuestDbDeploymentStatus) -> QuestDbDeployment:
    deployment = deployments[deployment_id]
    if deployment is None: raise Exception(f"Deployment with id {deployment_id} not found")

    updated_deployment = replace(deployment, status=status)
    deployments[deployment_id] = updated_deployment

    return updated_deployment


async def update_metadata(deployment_id: UUID, metadata: K8sMetadata) -> QuestDbDeployment:
    deployment = deployments[deployment_id]
    if deployment is None: raise Exception(f"Deployment with id {deployment_id} not found")

    updated_deployment = replace(deployment, k8s_metadata=metadata)
    deployments[deployment_id] = updated_deployment

    return updated_deployment
