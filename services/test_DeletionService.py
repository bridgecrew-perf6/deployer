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

    namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.ACTIVE)

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

    @patch("services.DeletionService.delete_service")
    @patch("services.DeletionService.delete_deployment")
    @patch("services.DeletionService.delete_volume_claim")
    @patch("services.DeletionService.delete_resource_quota")
    @patch("services.DeletionService.delete_namespace")
    async def test_delete_should_call_creation_steps(self, delete_namespace, delete_quota, delete_claim,
                                                     delete_deployment,
                                                     delete_service):
        deployment = QuestDbDeployment()

        delete_namespace.return_value = deployment
        delete_quota.return_value = deployment
        delete_claim.return_value = deployment
        delete_deployment.return_value = deployment
        delete_service.return_value = deployment

        await DeletionService.delete(deployment)

        delete_service.assert_called_once_with(deployment)
        delete_deployment.assert_called_once_with(deployment)
        delete_claim.assert_called_once_with(deployment)
        delete_quota.assert_called_once_with(deployment)
        delete_namespace.assert_called_once_with(deployment)

    @patch("clients.k8s.ServiceClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_service_should_call_client_and_persist_result(self, update_metadata,
                                                                        delete_service_client):
        deployment = get_created_deployment()
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, service=None))

        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete_service(deployment)

        delete_service_client.assert_called_once_with(deployment.k8s_metadata.namespace.name,
                                                      deployment.k8s_metadata.service.id)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.DeploymentClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_deployment_should_call_client_and_persist_result(self, update_metadata,
                                                                           delete_deployment_client):
        deployment = get_created_deployment()
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, deployment=None))

        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete_deployment(deployment)

        delete_deployment_client.assert_called_once_with(deployment.k8s_metadata.namespace.name,
                                                         deployment.k8s_metadata.deployment.id)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.VolumeClaimClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_volume_claim_should_call_client_and_persist_result(self, update_metadata,
                                                                             delete_claim_client):
        deployment = get_created_deployment()
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, volume_claim=None))

        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete_volume_claim(deployment)

        delete_claim_client.assert_called_once_with(deployment.k8s_metadata.namespace.name,
                                                    deployment.k8s_metadata.volume_claim.id)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.ResourceQuotaClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_resource_quota_should_call_client_and_persist_result(self, update_metadata,
                                                                               delete_quota_client):
        deployment = get_created_deployment()
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, resource_quota=None))

        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete_resource_quota(deployment)

        delete_quota_client.assert_called_once_with(deployment.k8s_metadata.namespace.name,
                                                    deployment.k8s_metadata.resource_quota.id)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.NamespaceClient.delete")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_delete_namespace_should_call_client_and_persist_result(self, update_metadata,
                                                                          delete_namespace_client):
        deployment = QuestDbDeployment()
        namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.TERMINATING)
        updated_deployment = replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, namespace=namespace))

        delete_namespace_client.return_value = namespace
        update_metadata.return_value = updated_deployment

        result = await DeletionService.delete_namespace(deployment)

        delete_namespace_client.assert_called_once_with(namespace.name)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)
