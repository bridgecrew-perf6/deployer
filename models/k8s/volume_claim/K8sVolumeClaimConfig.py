from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class K8sVolumeClaimConfig(JSONWizard):
    storage: str
