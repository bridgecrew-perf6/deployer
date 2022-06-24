from copy import deepcopy

from kubernetes_asyncio.client import V1ResourceQuota
from kubernetes_asyncio.client.exceptions import ApiException

from models.k8s.resource_quota.K8sResourceQuota import K8sResourceQuota
from models.k8s.resource_quota.K8sResourceQuotaConfig import K8sResourceQuotaConfig
from .client import get_core_client
from .templates import resource_quota_template


async def create(namespace: str, config: K8sResourceQuotaConfig) -> K8sResourceQuota:
    template = deepcopy(resource_quota_template)
    template['metadata']['name'] = f"quota-{namespace}"
    template['spec']['hard']['cpu'] = config.cpu
    template['spec']['hard']['memory'] = config.memory
    core_client = get_core_client()
    response: V1ResourceQuota = await core_client.create_namespaced_resource_quota(namespace, template)

    return K8sResourceQuota(id=response.metadata.name, config=config)


async def refresh(namespace: str, quota: K8sResourceQuota | None) -> K8sResourceQuota | None:
    if quota is None: return None

    core_client = get_core_client()
    try:
        await core_client.read_namespaced_resource_quota(quota.id, namespace)
    except ApiException as error:
        if error.status == 404:
            return None
        else:
            raise error

    return quota
