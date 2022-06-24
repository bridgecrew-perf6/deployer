from dataclasses import replace

from models.QuestDbDeployment import QuestDbDeployment
from models.k8s.deployment.K8sDeployment import K8sDeployment
from models.k8s.deployment.K8sDeploymentConfig import K8sDeploymentConfig
from models.k8s.deployment.K8sDeploymentStatus import K8sDeploymentStatus
from models.k8s.namespace.K8sNamespace import K8sNamespace
from models.k8s.namespace.K8sNamespacePhase import K8sNamespacePhase
from models.k8s.resource_quota.K8sResourceQuota import K8sResourceQuota
from models.k8s.resource_quota.K8sResourceQuotaConfig import K8sResourceQuotaConfig
from models.k8s.service.K8sService import K8sService
from models.k8s.service.K8sServiceConfig import K8sServiceConfig
from models.k8s.volume_claim.K8sVolumeClaim import K8sVolumeClaim
from models.k8s.volume_claim.K8sVolumeClaimConfig import K8sVolumeClaimConfig


def get_deployment_with_namespace():
    deployment = QuestDbDeployment()
    namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.Active)
    metadata = replace(deployment.k8s_metadata, namespace=namespace)
    return replace(deployment, k8s_metadata=metadata)


def get_deployment_with_namespace_quota_and_volume_claim():
    deployment = get_deployment_with_namespace()
    resource_quota_config = K8sResourceQuotaConfig("1000", "1Gi")
    resource_quota = K8sResourceQuota(str(deployment.id), resource_quota_config)

    volume_claim_config = K8sVolumeClaimConfig("1Gi")
    volume_claim = K8sVolumeClaim(str(deployment.id), volume_claim_config)
    metadata = replace(deployment.k8s_metadata, volume_claim=volume_claim, resource_quota=resource_quota)
    return replace(deployment, k8s_metadata=metadata)


def get_created_deployment():
    deployment = QuestDbDeployment()

    namespace = K8sNamespace(str(deployment.id), K8sNamespacePhase.Active)

    resource_quota_config = K8sResourceQuotaConfig("1000", "1Gi")
    resource_quota = K8sResourceQuota(str(deployment.id), resource_quota_config)

    volume_claim_config = K8sVolumeClaimConfig("1Gi")
    volume_claim = K8sVolumeClaim(str(deployment.id), volume_claim_config)

    deployment_config = K8sDeploymentConfig("1000", "1Gi", "1Gi")
    k8s_deployment = K8sDeployment(str(deployment.id), K8sDeploymentStatus.PROGRESSING, deployment_config)

    service_config = K8sServiceConfig("30000")
    service = K8sService(str(deployment.id), service_config)

    metadata = replace(deployment.k8s_metadata,
                       namespace=namespace,
                       resource_quota=resource_quota,
                       volume_claim=volume_claim,
                       deployment=k8s_deployment,
                       service=service)
    return replace(deployment, k8s_metadata=metadata)
