from models.k8s.namespace import K8sNamespace
from models.k8s.service import K8sService, K8sServiceConfig


async def create(namespace: K8sNamespace, config: K8sServiceConfig) -> K8sService:
    raise Exception("Not implemented")


async def delete(namespace: K8sNamespace, service_id: str) -> K8sService:
    raise Exception("Not implemented")


async def read(namespace: K8sNamespace, service_id: str) -> K8sService:
    raise Exception("Not implemented")