import os
import yaml
import logging

from models.base import Base

LEVELS = ("debug", "info", "warning", "error")


class Config(Base):

    def __init__(self, filepath: str = None):
        self.filepath = filepath
        self.TOKEN = None
        self.HOST = None
        self.PORT = None
        self.LOGLEVEL = self.__convert_loglevel("info")

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
                value = self.__convert_loglevel(value)
            setattr(self, key.upper(), value)

    def __convert_loglevel(self, level: str):
        error_msg = "loglevel must be: debug/info/warning/error"
        if level.lower() not in LEVELS:
            raise ValueError(error_msg)

        loglevel = getattr(logging, level.upper())
        if not isinstance(loglevel, int):
            raise ValueError(error_msg)

        return loglevel
