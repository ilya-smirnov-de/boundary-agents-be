from pathlib import Path
import json
import os
import logging

import constants


class Configuration:
    def __init__(self):
        self.config = None
        self._config_file = None
        conf_path = str("./config")
        # Use the environment variable CONF_PATH to set configuration path /data in Docker
        if os.environ.get("CONF_PATH") is not None:
            conf_path = os.environ["CONF_PATH"]
        self._config_file = str(conf_path + "/config.json")
        logging.info("Using configuration file from %s", self._config_file)
        self.config = json.loads(Path(self._config_file).read_text(encoding='utf-8'))
        if self.config is None:
            logging.critical("Fatal error, configuration failed (%s)", self._config_file)
            exit(1)

    def get_config(self):
        return self.config

    def get_fact_grid_url(self) -> str:
        return self.config["fact-grid-url"]

    def get_fact_grid_entity_data_url(self) -> str:
        return self.config["fact-grid-entity-data-url"]

    def get_port(self) -> int:
        return int(self.config["port"])
