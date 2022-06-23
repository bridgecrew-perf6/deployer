from copy import deepcopy

from kubernetes_asyncio.client import V1Deployment

from models.k8s.deployment.K8sDeployment import K8sDeployment
from models.k8s.deployment.K8sDeploymentConfig import K8sDeploymentConfig
from models.k8s.deployment.K8sDeploymentStatus import K8sDeploymentStatus
from .client import get_apps_client
from .templates import deployment_template


async def create(namespace: str, config: K8sDeploymentConfig) -> K8sDeployment:
    template = deepcopy(deployment_template)
    template['metadata']['name'] = f"deployment-{namespace}"
    template['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = config.memory
    template['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = config.cpu
    template['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = config.memory
    template['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = config.cpu
    template['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] = config.claim_name
    apps_client = get_apps_client()
    response: V1Deployment = await apps_client.create_namespaced_deployment(namespace, template)

    status = calculate_deployment_status(response)
    return K8sDeployment(id=response.metadata.name, config=config, status=status)


async def delete(namespace: str, deployment_id: str) -> K8sDeployment:
    raise Exception("Not implemented")


async def read(namespace: str, deployment_id: str) -> K8sDeployment:
    raise Exception("Not implemented")


def calculate_deployment_status(deployment_response: V1Deployment) -> K8sDeploymentStatus:
    conditions = deployment_response.status.conditions

    if conditions is None:
        return K8sDeploymentStatus.PROGRESSING

    if next((condition for condition in conditions if
             condition['type'] == 'Progressing' and
             condition['status'] == 'True' and
             condition['reason'] == 'NewReplicaSetAvailable'), False):
        return K8sDeploymentStatus.COMPLETE

    if next((condition for condition in conditions if
             condition['type'] == 'Progressing' and
             condition['status'] == 'False'), False):
        return K8sDeploymentStatus.FAILED

    if next((condition for condition in conditions if
             condition['type'] == 'Available' and
             condition['status'] == 'False'), False):
        return K8sDeploymentStatus.FAILED

    return K8sDeploymentStatus.PROGRESSING
