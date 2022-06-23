from copy import deepcopy

from kubernetes_asyncio.client import V1Service

from models.k8s.service.K8sService import K8sService
from models.k8s.service.K8sServiceConfig import K8sServiceConfig
from .client import get_core_client
from .templates import service_template


async def create(namespace: str) -> K8sService:
    template = deepcopy(service_template)
    template['metadata']['name'] = f"service-{namespace}"
    core_client = get_core_client()
    response: V1Service = await core_client.create_namespaced_service(namespace, template)

    return K8sService(id=response.metadata.name,
                      config=K8sServiceConfig(node_port=str(response.spec.ports[0].node_port)))


async def delete(namespace: str, service_id: str) -> K8sService:
    raise Exception("Not implemented")


async def read(namespace: str, service_id: str) -> K8sService:
    raise Exception("Not implemented")
