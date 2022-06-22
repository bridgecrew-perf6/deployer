from dataclasses import dataclass
from models.k8s.namespace.K8sNamespace import K8sNamespace
from models.k8s.resource_quota.K8sResourceQuota import K8sResourceQuota
from models.k8s.volume_claim.K8sVolumeClaim import K8sVolumeClaim
from models.k8s.deployment.K8sDeployment import K8sDeployment
from models.k8s.service.K8sService import K8sService


@dataclass
class K8sMetadata:
    namespace: K8sNamespace | None = None
    resource_quota: K8sResourceQuota | None = None
    volume_claim: K8sVolumeClaim | None = None
    deployment: K8sDeployment | None = None
    service: K8sService | None = None
