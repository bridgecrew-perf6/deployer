import json
from copy import deepcopy
from dataclasses import replace

from kubernetes_asyncio.client import V1Status, V1Namespace
from kubernetes_asyncio.client.exceptions import ApiException

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


async def delete(name: str) -> K8sNamespace | None:
    core_client = get_core_client()
    response: V1Status = await core_client.delete_namespace(name)
    phase = json.loads(response.status.replace("'", "\""))['phase']

    return K8sNamespace(name=name, phase=K8sNamespacePhase[phase])


async def refresh(namespace: K8sNamespace | None) -> K8sNamespace | None:
    if namespace is None: return None

    core_client = get_core_client()
    try:
        response: V1Namespace = await core_client.read_namespace(namespace.name)
    except ApiException as error:
        if error.status == 404:
            return None
        else:
            raise error

    return replace(namespace, phase=K8sNamespacePhase[response.status.phase])
