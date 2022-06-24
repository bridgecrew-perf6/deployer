from dataclasses import replace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import services.DeletionService as DeletionService
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from services.testutils import get_created_deployment


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
