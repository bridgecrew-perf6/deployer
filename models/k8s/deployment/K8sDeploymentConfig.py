from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class K8sDeploymentConfig(JSONWizard):
    memory: str
    cpu: str
    claim_name: str
