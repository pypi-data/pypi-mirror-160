"""Process execution"""

import pathlib

from python_json_config import ConfigBuilder
from python_json_config.config_node import Config

from mlengineerbelvo.pipeline.process import Process

BASE_CONFIG_FILE = "config/pipeline.json"


def load_configuration(
    config_file: str = BASE_CONFIG_FILE,
) -> Config:
    """Load Configuration file.

    Args:
        config_file (str, optional): JSON file with pipeline configuration.
         Defaults to BASE_CONFIG_FILE.

    Returns:
        Config: Configuration Node object with loaded configs.
    """
    builder = ConfigBuilder()
    config = builder.parse_config(pathlib.Path(config_file).resolve())
    return config


mlops_pipeline_process = Process(config=load_configuration())
mlops_pipeline_process.run()
