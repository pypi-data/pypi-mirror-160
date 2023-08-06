from pathlib import Path

# from .utils import in_container


# class PFS:
#
#     @staticmethod
#     def get(repo: str, out: bool = False) -> Path:
#         if in_container():
#             path = Path("/pfs", repo) if not out else Path("/pfs/out")
#             if not path.exists():
#                 raise NotADirectoryError(path)
#         else:
#             raise NotImplementedError(
#                 "TODO: Add connection with mount extension for local development"
#             )
#         return path

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PFS:
    repo: str
    name: Optional[str] = None
    branch: Optional[str] = None
    glob: Optional[str] = None

    def serialize(self):
        return {key: value for key, value in asdict(self).items() if value is not None}

    @property
    def mount_path(self) -> Path:
        # return Path.home().joinpath("pfs", self.name or self.repo)
        return Path("/pfs", self.name or self.repo)
