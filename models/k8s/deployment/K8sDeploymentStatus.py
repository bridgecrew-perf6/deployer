from enum import Enum


class K8sDeploymentStatus(Enum):
    PROGRESSING = "PROGRESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
