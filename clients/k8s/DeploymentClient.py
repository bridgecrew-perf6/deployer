from models.k8s.deployment import K8sDeployment, K8sDeploymentConfig
from models.k8s.namespace import K8sNamespace


async def create(namespace: K8sNamespace, config: K8sDeploymentConfig) -> K8sDeployment:
    raise Exception("Not implemented")


async def delete(namespace: K8sNamespace, deployment_id: str) -> K8sDeployment:
    raise Exception("Not implemented")


async def read(namespace: K8sNamespace, deployment_id: str) -> K8sDeployment:
    raise Exception("Not implemented")
