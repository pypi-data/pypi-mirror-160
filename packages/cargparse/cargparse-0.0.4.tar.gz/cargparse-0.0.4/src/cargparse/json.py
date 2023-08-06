import json
from pathlib import Path

from .namespace import Namespace


class JSON(Namespace):

    def load(self, filename: Path | str) -> list[str]:
        raise NotImplementedError("JSON config files are not (yet) supported")
