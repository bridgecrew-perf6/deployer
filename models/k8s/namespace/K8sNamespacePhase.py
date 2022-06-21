from enum import Enum


class K8sNamespacePhase(Enum):
    ACTIVE = "ACTIVE"
    TERMINATING = "TERMINATING"
