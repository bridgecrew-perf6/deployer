from dataclasses import dataclass
from datetime import datetime

from .K8sNamespacePhase import K8sNamespacePhase


@dataclass
class K8sNamespace:
    name: str
    phase: K8sNamespacePhase
    inserted_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
