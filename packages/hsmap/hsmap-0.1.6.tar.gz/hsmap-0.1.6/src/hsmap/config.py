import json
import os
from pathlib import Path
from typing import (
    Any,
    Dict,
)

import httpx


class ReadConfig:
    """
    read config from source.

    source priority:
        read form env `CONFIG_SOURCE` >> read from argument `config_source` >> config.json
    source format:
        json format from file or http get request

    """

    _default_source = "config.json"

    def __init__(self, root: Path = None, config_source: str = None):
        self.root: Path = root if root else Path(__file__).parents[0]
        self.config_source = os.getenv(
            "CONFIG_SOURCE", config_source or self._default_source
        )

    def read_from_json(self) -> dict:
        try:
            config_path = self.root / self.config_source
            return json.loads(config_path.read_bytes())
        except Exception as e:
            raise EnvironmentError("Load Config from json file Error!") from e

    def read_from_http(self) -> dict:
        try:
            return httpx.get(self.config_source).json()
        except Exception as e:
            raise EnvironmentError("Load Config from Net Server Error!") from e

    def load_config(self) -> Dict[str, Any]:
        if (
            self.config_source.lower().endswith(".json")
            and (self.root / self.config_source).exists()
        ):
            return self.read_from_json()

        elif self.config_source.lower().startswith("http"):
            return self.read_from_http()

        raise EnvironmentError("Please provide a correct CONFIG_SOURCE env")
