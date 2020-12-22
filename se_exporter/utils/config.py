#!/usr/bin/env python3
"""This module contains a Config for app."""

import yaml
from se_exporter.models.base import Base


class Config(Base):

    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.token = None
        self.host = None
        self.port = None
        self.listen_addr = "0.0.0.0"
        self.listen_port = 9122
        self.loglevel = "INFO"
        self.run_async = False

        self.__build()

    def __read(self):
        try:
            with open(self.filepath, "r") as cfgfile:
                data = yaml.load(cfgfile, Loader=yaml.Loader)
                return data
        except FileNotFoundError:
            raise RuntimeError("Config file not found")
        except TypeError:
            raise RuntimeError("Corrupted config file or bad format")

    def __build(self):
        if self.filepath is None:
            return

        config = self.__read()
        if config is None or not config:
            return

        for key, value in config.items():
            if key.lower() == "loglevel":
                value = value.upper()
            setattr(self, key, value)
