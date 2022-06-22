from models.k8s.namespace import K8sNamespace


async def create(name: str) -> K8sNamespace:
    raise Exception("Not implemented")


async def delete(name: str) -> K8sNamespace:
    raise Exception("Not implemented")


async def read(name: str) -> K8sNamespace:
    raise Exception("Not implemented")
