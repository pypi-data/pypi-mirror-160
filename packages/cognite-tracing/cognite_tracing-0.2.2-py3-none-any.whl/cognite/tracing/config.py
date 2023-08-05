from dataclasses import dataclass
from typing import Set


@dataclass
class TracingConfig:
    tags_to_inherit: Set[str]


config = TracingConfig(tags_to_inherit=set())
