import logging
from dataclasses import dataclass
from typing import Any, Dict

import dacite
import yaml
from dacite import MissingValueError
from sikriml.environment.configs import EnvironmentConfiguration
from sikriml.webservice.configs import DeploymentConfiguration


@dataclass
class MLConfiguration:
    environment: EnvironmentConfiguration
    deployment: DeploymentConfiguration


# define converters/validators for the various data types we use
converters: Dict[Any, Any] = {}


def get_ml_config(config_path: str) -> MLConfiguration:
    try:
        with open(config_path) as yaml_file:
            raw_cfg = yaml.safe_load(yaml_file)

        return dacite.from_dict(
            data_class=MLConfiguration,
            data=raw_cfg,
            config=dacite.Config(type_hooks=converters),
        )
    except FileNotFoundError:
        logging.error(f"Configuration error: can't find {config_path} file")
        raise
    except MissingValueError as err:
        logging.error(f"Configuration error: {str(err)}")
        raise
