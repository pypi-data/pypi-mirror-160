from typing import List, Optional

from dataclasses import dataclass

from .aci_config import AciConfiguration
from .aks_config import AksConfiguration


@dataclass
class DeploymentConfiguration:
    model_names: List[str]
    service_name: str
    cluster_name: Optional[str]
    compute_target_name: Optional[str]
    cluster_purpose: Optional[str]
    aci: Optional[AciConfiguration]
    aks: Optional[AksConfiguration]
