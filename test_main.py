from fastapi.testclient import TestClient

from main import app
from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus

client = TestClient(app)


def test_create_deployment():
    response = client.post("/")
    deployment = QuestDbDeployment.from_json(response.json())
    assert response.status_code == 200
    assert deployment.status == QuestDbDeploymentStatus.CREATION_SCHEDULED


def test_delete_deployment():
    deployment = QuestDbDeployment.from_json(client.post("/").json())

    response = client.delete(f"/{deployment.id}")
    deleted_deployment: QuestDbDeployment = QuestDbDeployment.from_json(response.json())

    assert response.status_code == 200
    assert deleted_deployment.id == deployment.id
    assert deleted_deployment.status == QuestDbDeploymentStatus.DELETION_SCHEDULED
