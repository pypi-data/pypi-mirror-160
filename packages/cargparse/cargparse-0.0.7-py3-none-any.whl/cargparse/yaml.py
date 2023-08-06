from __future__ import annotations

import argparse
from pathlib import Path

import yaml  # TODO: make third-party library installs optional depending on use

from .namespace import Namespace


class YAML(Namespace):

    def load(self, filename: Path | str) -> list[str]:

        extension = Path(filename).suffix

        if extension not in {'.yaml', '.yml'}:
            raise argparse.ArgumentError(
                argument=None,
                message=f"Cannot parse {extension} file with {self.__class__.__name__}",
            )

        with open(filename) as f:
            return self._dict_to_args(yaml.safe_load(f))
