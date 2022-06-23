from dataclasses import dataclass, field
from datetime import datetime

from dataclass_wizard import JSONWizard

from .K8sNamespacePhase import K8sNamespacePhase


@dataclass
class K8sNamespace(JSONWizard):
    name: str
    phase: K8sNamespacePhase
    inserted_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
