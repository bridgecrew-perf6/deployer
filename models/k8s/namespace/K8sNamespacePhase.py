from enum import Enum


class K8sNamespacePhase(Enum):
    Active = "Active"
    Terminating = "Terminating"
