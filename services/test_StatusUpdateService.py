from dataclasses import replace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, call

import services.StatusUpdateService as StatusUpdateService
from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from models.k8s.deployment.K8sDeploymentStatus import K8sDeploymentStatus
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from services.testutils import get_created_deployment


class StatusUpdateServiceTest(IsolatedAsyncioTestCase):

    @patch("repositories.QuestDbDeploymentRepo.find_not_in_statuses")
    @patch("services.StatusUpdateService.update_status")
    async def test_status_update_scheduler_should_update_status_of_each_deployment(self, update_status,
                                                                                   find_not_in_statuses):
        base_deployment = QuestDbDeployment()
        deployments = [
            base_deployment,
            replace(base_deployment, status=QuestDbDeploymentStatus.CREATION_PENDING),
            replace(base_deployment, status=QuestDbDeploymentStatus.RUNNING),
            replace(base_deployment, status=QuestDbDeploymentStatus.UPDATE_PENDING),
            replace(base_deployment, status=QuestDbDeploymentStatus.DEPLOYMENT_FAILED),
            replace(base_deployment, status=QuestDbDeploymentStatus.DELETION_SCHEDULED),
            replace(base_deployment, status=QuestDbDeploymentStatus.DELETION_PENDING),
        ]
        find_not_in_statuses.return_value = deployments

        await StatusUpdateService.schedule_status_updates()

        find_not_in_statuses.assert_called_once_with([QuestDbDeploymentStatus.DELETED, QuestDbDeploymentStatus.ERROR])

        update_status.assert_has_calls(map(lambda deployment: call(deployment), deployments))

    @patch("clients.k8s.NamespaceClient.refresh")
    @patch("clients.k8s.ResourceQuotaClient.refresh")
    @patch("clients.k8s.VolumeClaimClient.refresh")
    @patch("clients.k8s.DeploymentClient.refresh")
    @patch("clients.k8s.ServiceClient.refresh")
    @patch("services.StatusUpdateService.recalculate_deletion_status")
    @patch("services.StatusUpdateService.recalculate_running_status")
    @patch("repositories.QuestDbDeploymentRepo.update_status")
    async def test_status_update_should_get_all_resources_data_and_call_correct_recalculation(self, update_status,
                                                                                              recalculate_running_status,
                                                                                              recalculate_deletion_status,
                                                                                              get_service,
                                                                                              get_deployment,
                                                                                              get_volume_claim,
                                                                                              get_quota,
                                                                                              get_namespace):
        deployment = get_created_deployment()
        running_deployments = [
            deployment,
            replace(deployment, status=QuestDbDeploymentStatus.CREATION_PENDING),
            replace(deployment, status=QuestDbDeploymentStatus.RUNNING),
            replace(deployment, status=QuestDbDeploymentStatus.UPDATE_PENDING),
            replace(deployment, status=QuestDbDeploymentStatus.DEPLOYMENT_FAILED),
        ]
        deletion_deployments = [
            replace(deployment, status=QuestDbDeploymentStatus.DELETION_SCHEDULED),
            replace(deployment, status=QuestDbDeploymentStatus.DELETION_PENDING),
        ]

        recalculate_running_status.return_value = QuestDbDeploymentStatus.UPDATE_PENDING
        recalculate_deletion_status.return_value = QuestDbDeploymentStatus.DELETION_PENDING

        await StatusUpdateService.update_status(deployment)

        namespace = deployment.k8s_metadata.namespace.name
        get_namespace.assert_called_once_with(deployment.k8s_metadata.namespace)
        get_quota.assert_called_once_with(namespace, deployment.k8s_metadata.resource_quota)
        get_volume_claim.assert_called_once_with(namespace, deployment.k8s_metadata.volume_claim)
        get_deployment.assert_called_once_with(namespace, deployment.k8s_metadata.deployment)
        get_service.assert_called_once_with(namespace, deployment.k8s_metadata.service)

        for deployment in running_deployments:
            recalculate_running_status.reset_mock()
            update_status.reset_mock()

            await StatusUpdateService.update_status(deployment)

            recalculate_running_status.assert_called_once()
            update_status.assert_called_once_with(deployment.id, QuestDbDeploymentStatus.UPDATE_PENDING)

        for deployment in deletion_deployments:
            recalculate_deletion_status.reset_mock()
            update_status.reset_mock()

            await StatusUpdateService.update_status(deployment)

            recalculate_deletion_status.assert_called_once()
            update_status.assert_called_once_with(deployment.id, QuestDbDeploymentStatus.DELETION_PENDING)

    async def test_recalculate_running_status_should_return_error_when_some_of_the_resources_are_none(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, namespace=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, resource_quota=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, volume_claim=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, deployment=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, service=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

    async def test_recalculate_running_status_should_return_failed_when_deployment_status_is_failed(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata,
                                                     deployment=replace(deployment.k8s_metadata.deployment,
                                                                        status=K8sDeploymentStatus.FAILED))))
        self.assertEqual(status, QuestDbDeploymentStatus.DEPLOYMENT_FAILED)

    async def test_recalculate_running_status_should_return_running_when_deployment_status_is_complete(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata,
                                                     deployment=replace(deployment.k8s_metadata.deployment,
                                                                        status=K8sDeploymentStatus.COMPLETE))))
        self.assertEqual(status, QuestDbDeploymentStatus.RUNNING)

    async def test_recalculate_running_status_should_return_creation_pending_if_previous_state_is_creation_pending(
            self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, status=QuestDbDeploymentStatus.CREATION_PENDING))
        self.assertEqual(status, QuestDbDeploymentStatus.CREATION_PENDING)

    async def test_recalculate_running_status_should_return_update_pending_if_previous_state_is_not_creation_pending(
            self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_running_status(
            replace(deployment, status=QuestDbDeploymentStatus.RUNNING))
        self.assertEqual(status, QuestDbDeploymentStatus.UPDATE_PENDING)

    async def test_recalculate_deletion_status_should_return_deleted_if_namespace_is_none(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_deletion_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata, namespace=None)))
        self.assertEqual(status, QuestDbDeploymentStatus.DELETED)

    async def test_recalculate_deletion_status_should_return_error_if_namespace_phase_is_active(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_deletion_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata,
                                                     namespace=replace(deployment.k8s_metadata.namespace,
                                                                       phase=K8sNamespacePhase.Active))))
        self.assertEqual(status, QuestDbDeploymentStatus.ERROR)

    async def test_recalculate_deletion_status_should_return_error_if_namespace_phase_is_not_active(self):
        deployment = get_created_deployment()
        status = StatusUpdateService.recalculate_deletion_status(
            replace(deployment, k8s_metadata=replace(deployment.k8s_metadata,
                                                     namespace=replace(deployment.k8s_metadata.namespace,
                                                                       phase=K8sNamespacePhase.Terminating))))
        self.assertEqual(status, QuestDbDeploymentStatus.DELETION_PENDING)
