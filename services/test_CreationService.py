from dataclasses import replace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import services.CreationService as CreationService
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


def get_deployment_with_namespace():
    deployment = QuestDbDeployment()
    namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.ACTIVE)
    metadata = replace(deployment.k8s_metadata, namespace=namespace)
    return replace(deployment, k8s_metadata=metadata)


def get_deployment_with_namespace_quota_and_volume_claim():
    deployment = get_deployment_with_namespace()
    resource_quota_config = K8sResourceQuotaConfig("1000", "1Gi")
    resource_quota = K8sResourceQuota(str(deployment.id), resource_quota_config)

    volume_claim_config = K8sVolumeClaimConfig("1Gi")
    volume_claim = K8sVolumeClaim(str(deployment.id), volume_claim_config)
    metadata = replace(deployment.k8s_metadata, volume_claim=volume_claim, resource_quota=resource_quota)
    return replace(deployment, k8s_metadata=metadata)


class CreationServiceTest(IsolatedAsyncioTestCase):

    @patch("services.CreationService.create_service")
    @patch("services.CreationService.create_deployment")
    @patch("services.CreationService.create_volume_claim")
    @patch("services.CreationService.create_resource_quota")
    @patch("services.CreationService.create_namespace")
    async def test_create_should_call_creation_steps(self, create_namespace, create_quota, create_claim,
                                                     create_deployment,
                                                     create_service):
        deployment = QuestDbDeployment()

        create_namespace.return_value = deployment
        create_quota.return_value = deployment
        create_claim.return_value = deployment
        create_deployment.return_value = deployment
        create_service.return_value = deployment

        await CreationService.create(deployment)

        create_namespace.assert_called_once_with(deployment)
        create_quota.assert_called_once_with(deployment)
        create_claim.assert_called_once_with(deployment)
        create_deployment.assert_called_once_with(deployment)
        create_service.assert_called_once_with(deployment)

    @patch("clients.k8s.NamespaceClient.create")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_create_namespace_should_call_client_and_persist_result(self, update_metadata,
                                                                          create_namespace_client):
        deployment = QuestDbDeployment()
        namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.ACTIVE)
        updated_deployment = replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, namespace=namespace))

        create_namespace_client.return_value = namespace
        update_metadata.return_value = updated_deployment

        result = await CreationService.create_namespace(deployment)

        create_namespace_client.assert_called_once_with(namespace.name)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.ResourceQuotaClient.create")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_create_resource_quota_should_call_client_and_persist_result(self, update_metadata,
                                                                               create_quota_client):
        deployment = get_deployment_with_namespace()
        resource_quota_config = K8sResourceQuotaConfig("1000", "1Gi")
        resource_quota = K8sResourceQuota(str(deployment.id), resource_quota_config)
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, resource_quota=resource_quota))

        create_quota_client.return_value = resource_quota
        update_metadata.return_value = updated_deployment

        result = await CreationService.create_resource_quota(deployment)

        create_quota_client.assert_called_once_with(deployment.k8s_metadata.namespace.name, resource_quota_config)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.VolumeClaimClient.create")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_create_volume_claim_should_call_client_and_persist_result(self, update_metadata,
                                                                             create_claim_client):
        deployment = get_deployment_with_namespace()
        volume_claim_config = K8sVolumeClaimConfig("1Gi")
        volume_claim = K8sVolumeClaim(str(deployment.id), volume_claim_config)
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, volume_claim=volume_claim))

        create_claim_client.return_value = volume_claim
        update_metadata.return_value = updated_deployment

        result = await CreationService.create_volume_claim(deployment)

        create_claim_client.assert_called_once_with(deployment.k8s_metadata.namespace.name, volume_claim_config)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.DeploymentClient.create")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_create_deployment_should_call_client_and_persist_result(self, update_metadata,
                                                                           create_deployment_client):
        deployment = get_deployment_with_namespace_quota_and_volume_claim()
        deployment_config = K8sDeploymentConfig(
            cpu=deployment.k8s_metadata.resource_quota.config.cpu,
            memory=deployment.k8s_metadata.resource_quota.config.memory,
            storage=deployment.k8s_metadata.volume_claim.config.storage,
        )
        k8s_deployment = K8sDeployment(str(deployment.id), K8sDeploymentStatus.PROGRESSING, deployment_config)
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, deployment=k8s_deployment))

        create_deployment_client.return_value = k8s_deployment
        update_metadata.return_value = updated_deployment

        result = await CreationService.create_deployment(deployment)

        create_deployment_client.assert_called_once_with(deployment.k8s_metadata.namespace.name, deployment_config)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)

    @patch("clients.k8s.ServiceClient.create")
    @patch("repositories.QuestDbDeploymentRepo.update_metadata")
    async def test_create_service_should_call_client_and_persist_result(self, update_metadata,
                                                                        create_service_client):
        deployment = get_deployment_with_namespace()
        service_config = K8sServiceConfig("30000")
        k8s_service = K8sService(str(deployment.id), service_config)
        updated_deployment = replace(deployment,
                                     k8s_metadata=replace(deployment.k8s_metadata, service=k8s_service))

        create_service_client.return_value = k8s_service
        update_metadata.return_value = updated_deployment

        result = await CreationService.create_service(deployment)

        create_service_client.assert_called_once_with(deployment.k8s_metadata.namespace.name)
        update_metadata.assert_called_once_with(updated_deployment.id, updated_deployment.k8s_metadata)
        self.assertEqual(result, updated_deployment)
