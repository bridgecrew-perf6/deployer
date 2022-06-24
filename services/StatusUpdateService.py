from asyncio import gather
from dataclasses import replace

from fastapi_utils.tasks import repeat_every

from clients.k8s import NamespaceClient, ResourceQuotaClient, VolumeClaimClient, DeploymentClient, ServiceClient
from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from models.k8s.deployment.K8sDeploymentStatus import K8sDeploymentStatus
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from repositories import QuestDbDeploymentRepo


async def schedule_status_updates():
    deployments_to_update = await QuestDbDeploymentRepo.find_not_in_statuses(
        [QuestDbDeploymentStatus.DELETED, QuestDbDeploymentStatus.ERROR])
    await gather(*map(update_status, deployments_to_update))


async def update_status(deployment: QuestDbDeployment):
    updated_deployment = await get_updated_deployment(deployment)
    if deployment.status in [QuestDbDeploymentStatus.DELETION_SCHEDULED, QuestDbDeploymentStatus.DELETION_PENDING]:
        new_status = recalculate_deletion_status(updated_deployment)
    else:
        new_status = recalculate_running_status(updated_deployment)

    await QuestDbDeploymentRepo.update_status(deployment.id, new_status)


async def get_updated_deployment(deployment: QuestDbDeployment) -> QuestDbDeployment:
    namespace = deployment.k8s_metadata.namespace.name
    updated_namespace = await NamespaceClient.refresh(deployment.k8s_metadata.namespace)
    updated_quota = await ResourceQuotaClient.refresh(namespace, deployment.k8s_metadata.resource_quota)
    updated_volume_claim = await VolumeClaimClient.refresh(namespace, deployment.k8s_metadata.volume_claim)
    updated_deployment = await DeploymentClient.refresh(namespace, deployment.k8s_metadata.deployment)
    updated_service = await ServiceClient.refresh(namespace, deployment.k8s_metadata.service)
    return replace(deployment, k8s_metadata=replace(deployment.k8s_metadata,
                                                    namespace=updated_namespace,
                                                    resource_quota=updated_quota,
                                                    volume_claim=updated_volume_claim,
                                                    deployment=updated_deployment,
                                                    service=updated_service))


def recalculate_running_status(deployment: QuestDbDeployment) -> QuestDbDeploymentStatus:
    metadata = deployment.k8s_metadata

    if None in [metadata.namespace, metadata.resource_quota, metadata.volume_claim, metadata.deployment,
                metadata.service]:
        return QuestDbDeploymentStatus.ERROR

    if metadata.deployment.status == K8sDeploymentStatus.FAILED:
        return QuestDbDeploymentStatus.DEPLOYMENT_FAILED

    if metadata.deployment.status == K8sDeploymentStatus.COMPLETE:
        return QuestDbDeploymentStatus.RUNNING

    if deployment.status == QuestDbDeploymentStatus.CREATION_PENDING:
        return QuestDbDeploymentStatus.CREATION_PENDING
    else:
        return QuestDbDeploymentStatus.UPDATE_PENDING


def recalculate_deletion_status(deployment: QuestDbDeployment) -> QuestDbDeploymentStatus:
    metadata = deployment.k8s_metadata

    if metadata.namespace is None:
        return QuestDbDeploymentStatus.DELETED

    if metadata.namespace.phase == K8sNamespacePhase.Active:
        return QuestDbDeploymentStatus.ERROR

    return QuestDbDeploymentStatus.DELETION_PENDING
