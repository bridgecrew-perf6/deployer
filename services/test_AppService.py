from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
import services.AppService as AppService
from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from dataclasses import replace


class AppServiceTest(IsolatedAsyncioTestCase):

    @patch("repositories.QuestDbDeploymentRepo.create")
    @patch("services.CreationService.create")
    async def test_create_should_call_create_entity_and_start_deployment(self, creation_service, repo_create):
        deployment = QuestDbDeployment()
        repo_create.return_value = deployment

        resulting_deployment = replace(deployment, status = QuestDbDeploymentStatus.CREATION_PENDING)
        creation_service.return_value = resulting_deployment

        result = await AppService.create()

        repo_create.assert_called_once()
        creation_service.assert_called_once_with(deployment)
        self.assertEqual(resulting_deployment, result)

    @patch("repositories.QuestDbDeploymentRepo.update_status")
    @patch("services.DeletionService.delete")
    async def test_delete_should_update_status_and_start_deletion(self, deletion_service, repo_update_status):
        deployment = QuestDbDeployment(status = QuestDbDeploymentStatus.DELETION_SCHEDULED)
        repo_update_status.return_value = deployment

        resulting_deployment = replace(deployment, status = QuestDbDeploymentStatus.DELETION_PENDING)
        deletion_service.return_value = resulting_deployment

        result = await AppService.delete(deployment.id)

        repo_update_status.assert_called_once_with(deployment.id, QuestDbDeploymentStatus.DELETION_SCHEDULED)
        deletion_service.assert_called_once_with(deployment)
        self.assertEqual(resulting_deployment, result)

    @patch("repositories.QuestDbDeploymentRepo.get")
    async def test_get_should_return_entity(self, repo_get):
        deployment = QuestDbDeployment()
        repo_get.return_value = deployment

        result = await AppService.get(deployment.id)

        repo_get.assert_called_once_with(deployment.id)
        self.assertEqual(deployment, result)
