from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class K8sServiceConfig(JSONWizard):
    node_port: str
