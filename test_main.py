from fastapi.testclient import TestClient
from models.QuestDbDeployment import QuestDbDeployment
from models.QuestDbDeploymentStatus import QuestDbDeploymentStatus
from main import app

client = TestClient(app)


def test_create_deployment():
    response = client.post("/")
    assert response.status_code == 200
    assert response.json() == QuestDbDeployment()


def test_delete_deployment():
    deployment: QuestDbDeployment = client.post("/").json()

    response = client.delete(f"/{deployment.id}")
    deleted_deployment: QuestDbDeployment = response.json()

    assert response.status_code == 200
    assert deleted_deployment.id == deployment.id
    assert deleted_deployment.status == QuestDbDeploymentStatus.DELETION_SCHEDULED


def test_get_deployment_status():
    deployment: QuestDbDeployment = client.post("/").json()
    # TODO: add mocks for kubernetes and mock background and repeatable job timers

    response = client.get(f"/{deployment.id}")
    updated_deployment: QuestDbDeployment = response.json()

    assert response.status_code == 200
    assert updated_deployment.id == deployment.id
    assert updated_deployment.status == QuestDbDeploymentStatus.UPDATE_PENDING
