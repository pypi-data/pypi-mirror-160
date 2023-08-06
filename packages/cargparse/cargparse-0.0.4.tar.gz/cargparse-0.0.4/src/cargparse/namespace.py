from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable


class Namespace:
    """
    Base class for parsing configuration files.

    You must supply an ArgumentParser object that defines the arguments for your project with
    FLAGGED arguments. Positional arguments will not work. If you want to make an argument
    required, use `parser.add_argument('--flag', required=True)`
    """

    def __init__(
        self,
        parser: argparse.ArgumentParser,
        filename: Path | str | None = None,
        arg_dict: dict[str, Any] | None = None,
    ) -> None:

        if filename and arg_dict:
            raise argparse.ArgumentError(
                argument=None,
                message=f"{self.__class__.__name__} cannot load both `filename` and `arg_dict",
            )
        elif not (filename or arg_dict):
            raise argparse.ArgumentError(
                argument=None,
                message=f"You must pass `filename` or `arg_dict` to {self.__class__.__name__}",
            )
        
        # convert key-value pairs to a regular list
        args: list[str] = self.load(filename) if filename else self._dict_to_args(arg_dict)

        # parse the list and validate types with Argument Parser
        self.namespace = parser.parse_args(args)

        # update namespace so arguments can be accessed as attributes
        self.__dict__.update(**vars(self.namespace))


    def _dict_to_args(self, x: dict | str) -> list[str]:

        arg_dict = []
        for key, value in eval(str(x)).items():
            arg_dict.append(f"--{key}")
            arg_dict.append(str(value))
        return arg_dict


    def load(self, filename: Path | str) -> list[str]:
        raise RuntimeError(
            "You must use a derivative of cargparse.Namespace to load a file (ex. YAMLNamespace)",
        )


    def __getattr__(self, name: str) -> Any:
        if name not in self.namespace:

            # TODO: search all keys and show tree if it occurs elsewhere

            raise AttributeError(
                f"{name} not in {self.__class__.__name__} {sorted(vars(self).keys())}",
            )
        return super().__getattribute__(name)


    def __repr__(self) -> str:
        return str(self.namespace)


    @classmethod
    def merge(self, namespaces: Iterable[Namespace]) -> Namespace:
        raise NotImplementedError(
            f"Combining {self.__class__.__name__} is not (yet) supported"
        )
