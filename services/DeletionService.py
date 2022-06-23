from dataclasses import replace

from clients.k8s import NamespaceClient, ResourceQuotaClient, VolumeClaimClient, DeploymentClient, ServiceClient
from models.QuestDbDeployment import QuestDbDeployment
from repositories import QuestDbDeploymentRepo


async def delete(deployment: QuestDbDeployment) -> QuestDbDeployment:
    deployment = await delete_service(deployment)
    deployment = await delete_deployment(deployment)
    deployment = await delete_volume_claim(deployment)
    deployment = await delete_resource_quota(deployment)
    return await delete_namespace(deployment)


async def delete_service(deployment: QuestDbDeployment) -> QuestDbDeployment:
    await ServiceClient.delete(deployment.k8s_metadata.namespace.name, deployment.k8s_metadata.service.id)
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, service=None))


async def delete_deployment(deployment: QuestDbDeployment) -> QuestDbDeployment:
    await DeploymentClient.delete(deployment.k8s_metadata.namespace.name, deployment.k8s_metadata.deployment.id)
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, deployment=None))


async def delete_volume_claim(deployment: QuestDbDeployment) -> QuestDbDeployment:
    await VolumeClaimClient.delete(deployment.k8s_metadata.namespace.name, deployment.k8s_metadata.volume_claim.id)
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, volume_claim=None))


async def delete_resource_quota(deployment: QuestDbDeployment) -> QuestDbDeployment:
    await ResourceQuotaClient.delete(deployment.k8s_metadata.namespace.name, deployment.k8s_metadata.resource_quota.id)
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, resource_quota=None))


async def delete_namespace(deployment: QuestDbDeployment) -> QuestDbDeployment:
    namespace = await NamespaceClient.delete(str(deployment.id))
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, namespace=namespace))
