from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class K8sResourceQuotaConfig(JSONWizard):
    memory: str
    cpu: str
