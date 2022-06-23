from dataclasses import replace

from clients.k8s import NamespaceClient
from models.QuestDbDeployment import QuestDbDeployment
from repositories import QuestDbDeploymentRepo


async def delete(deployment: QuestDbDeployment) -> QuestDbDeployment:
    namespace = await NamespaceClient.delete(str(deployment.id))
    return await QuestDbDeploymentRepo.update_metadata(deployment.id,
                                                       replace(deployment.k8s_metadata, namespace=namespace,
                                                               service=None, deployment=None, volume_claim=None,
                                                               resource_quota=None))
