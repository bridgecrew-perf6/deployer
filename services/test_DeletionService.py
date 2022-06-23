from dataclasses import replace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import services.DeletionService as DeletionService
from models.QuestDbDeployment import QuestDbDeployment
from models.k8s.deployment.K8sDeployment import K8sDeployment
from models.k8s.deployment.K8sDeploymentConfig import K8sDeploymentConfig
from models.k8s.deployment.K8sDeploymentStatus import K8sDeploymentStatus
from models.k8s.namespace.K8sNamespace import K8sNamespace
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from models.k8s.resource_quota.K8sResourceQuota import K8sResourceQuota
from models.k8s.resource_quota.K8sResourceQuotaConfig import K8sResourceQuotaConfig
from models.k8s.service.K8sService import K8sService
from models.k8s.service.K8sServiceConfig import K8sServiceConfig
from models.k8s.volume_claim.K8sVolumeClaim import K8sVolumeClaim
from models.k8s.volume_claim.K8sVolumeClaimConfig import K8sVolumeClaimConfig


def get_created_deployment():
    deployment = QuestDbDeployment()

    namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.Active)

    resource_quota_config = K8sResourceQuotaConfig("1000", "1Gi")
    resource_quota = K8sResourceQuota(str(deployment.id), resource_quota_config)

    volume_claim_config = K8sVolumeClaimConfig("1Gi")
    volume_claim = K8sVolumeClaim(str(deployment.id), volume_claim_config)

    deployment_config = K8sDeploymentConfig("1000", "1Gi", "1Gi")
    k8s_deployment = K8sDeployment(str(deployment.id), K8sDeploymentStatus.PROGRESSING, deployment_config)

    service_config = K8sServiceConfig("30000")
    service = K8sService(str(deployment.id), service_config)

    metadata = replace(deployment.k8s_metadata,
                       namespace=namespace,
                       resource_quota=resource_quota,
                       volume_claim=volume_claim,
                       deployment=k8s_deployment,
                       service=service)
    return replace(deployment, k8s_metadata=metadata)


class DeletionServiceTest(IsolatedAsyncioTestCase):

    @patch("clients.k8s.NamespaceClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_should_call_namespace_deletion_client_and_persist_state(self, update_metadata,
                                                                                  delete_service_client):
        deployment = get_created_deployment()
        namespace = replace(deployment.k8s_metadata.namespace, phase=K8sNamespacePhase.Terminating)
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(
                                         deployment.k8s_metadata, namespace=namespace,
                                         service=None, deployment=None, volume_claim=None, resource_quota=None))

        delete_service_client.return_value = namespace
        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete(deployment)

        delete_service_client.assert_called_once_with(deployment.k8s_metadata.namespace.name)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)
