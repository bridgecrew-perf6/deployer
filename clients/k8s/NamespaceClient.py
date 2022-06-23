from copy import deepcopy

from kubernetes_asyncio.client import V1Namespace

from models.k8s.namespace.K8sNamespace import K8sNamespace
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from .client import get_core_client
from .templates import namespace_template


async def create(name: str) -> K8sNamespace:
    template = deepcopy(namespace_template)
    template['metadata']['name'] = name
    core_client = get_core_client()
    response: V1Namespace = await core_client.create_namespace(template)

    return K8sNamespace(name=response.metadata.name, phase=K8sNamespacePhase[response.status.phase])


async def delete(name: str) -> K8sNamespace:
    raise Exception("Not implemented")


async def read(name: str) -> K8sNamespace:
    raise Exception("Not implemented")
