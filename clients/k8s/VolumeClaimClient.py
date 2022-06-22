from models.k8s.namespace import K8sNamespace
from models.k8s.volume_claim import K8sVolumeClaim


async def create(namespace: K8sNamespace) -> K8sVolumeClaim:
    raise Exception("Not implemented")


async def delete(namespace: K8sNamespace, claim_id: str) -> K8sVolumeClaim:
    raise Exception("Not implemented")


async def read(namespace: K8sNamespace, claim_id: str) -> K8sVolumeClaim:
    raise Exception("Not implemented")
