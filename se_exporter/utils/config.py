#!/usr/bin/env python3
"""This module contains a Config for app."""

import yaml

from models.base import Base


class Config(Base):

    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.TOKEN = None
        self.HOST = None
        self.PORT = None
        self.LISTEN_ADDR = "0.0.0.0"
        self.LISTEN_PORT = 9122
        self.LOGLEVEL = "INFO"
        self.RUN_ASYNC = False

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
            setattr(self, key.upper(), value)
