from typing import Optional

from dataclasses import dataclass


@dataclass
class EnvironmentConfiguration:
    name: str
    version: Optional[str]
    build_timeout: Optional[int]
