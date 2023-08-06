import os

from dataclasses import dataclass
from types import ModuleType


@dataclass
class PipelineSource:
    module: ModuleType
    location: os.PathLike
    original: bytes
    script: bytes
