#!/usr/bin/env python3
"""This module contains Base parent class."""

import json
import logging
from abc import ABCMeta

logger = logging.getLogger(__name__)


class Base(object):
    """Base class for metrics objects."""

    __metaclass__ = ABCMeta

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self.__dict__[item]

    @staticmethod
    def handle_unknown_kwargs(obj, **kwargs):
        if kwargs:
            logger.debug("Unparsed fields from API")
            logger.debug(f"Type: {type(obj)}; kwargs: {kwargs}")

    @classmethod
    def de_json(cls, data, client: object = None):
        """Deserialize object."""
        if not data:
            return None

        data = data.copy()
        return data

    def to_json(self):
        """Serialize object to json."""
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Recursive serialize object."""

        def parse(val):
            if isinstance(val, list):
                return [parse(it) for it in val]
            elif isinstance(val, dict):
                return {key: parse(value) for key, value in val.items() if not key.startswith("_")}
            else:
                return val

        data = self.__dict__.copy()
        return parse(data)
