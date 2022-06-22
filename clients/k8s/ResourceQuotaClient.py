from models.k8s.namespace import K8sNamespace
from models.k8s.resource_quota import K8sResourceQuota, K8sResourceQuotaConfig


async def create(namespace: K8sNamespace, config: K8sResourceQuotaConfig) -> K8sResourceQuota:
    raise Exception("Not implemented")


async def delete(namespace: K8sNamespace, quota_id: str) -> K8sResourceQuota:
    raise Exception("Not implemented")


async def read(namespace: K8sNamespace, quota_id: str) -> K8sResourceQuota:
    raise Exception("Not implemented")
