#!/usr/bin/env python3

import hmac
import random
import base64
import hashlib
import asyncio
import aiohttp
import requests
import logging

from aiohttp.client_exceptions import (
    ContentTypeError,
)

from wsgiref.handlers import format_date_time
from datetime import datetime as dt
from itertools import count
from time import time, mktime

from models.base import Base

logger = logging.getLogger(__name__)


class VRageAPI(Base):
    """Asyncronous client for VRage Remote API.

    Arguments:
      :host: str
      :token: str
      :port: int

    """

    def __init__(
        self,
        host: str,
        token: str,
        port: int = 8080
    ):

        if not isinstance(host, str):
            raise RuntimeError("Bad host format")

        self.host = self.__verify_host(host)
        self.port = port
        self.token = token
        self.basepath = "/vrageremote/v1"
        self.endpoint = f"{self.host}:{self.port}{self.basepath}"
        self.nonce = count(int(time() * random.randint(10, 100)))
        logger.debug(f"VRageAPI client ready: {self}")

    def __verify_host(self, host: str):
        if not host.startswith("http://"):
            return f"http://{host}"

    def __date(self):
        return format_date_time(
            mktime(dt.now().timetuple())
        )

    def __hash(self, uri: str, dtime: str):
        nonce = str(next(self.nonce))
        salt = f"{uri}\r\n{nonce}\r\n{dtime}\r\n"
        token = base64.b64decode(self.token)

        signature = hmac.new(
            token,
            salt.encode("utf-8"),
            hashlib.sha1
        )

        salted_hash = base64.b64encode(signature.digest()).decode()
        result = f"{nonce}:{salted_hash}"

        return result

    def __prepare_request(self, path: str):
        if not path.startswith("/"):
            path = f"/{path}"

        dtime = self.__date()
        url = self.endpoint + path

        resource_fullpath = self.basepath + path
        authorization = self.__hash(resource_fullpath, dtime)
        headers = dict(Date=dtime, Authorization=authorization)

        return url, headers

    def __mapping(self, data: str):
        gauge = (
            "Asteroids", "Grids", "Planets", "BannedPlayers",
            "Characters", "KickedPlayers", "FloatingObjects"
        )

        if not isinstance(data, dict):
            return

        resources = data.get("data")
        if len(resources) < 1:
            return

        resource_name = list(resources.keys())[0]
        if resource_name in gauge:
            return {
                resource_name: {
                    "count": len(resources[resource_name]),
                    "objects": resources[resource_name]
                }
            }
        else:
            return resources

    async def aioget_metric(self, name: str):
        url, headers = self.__prepare_request(name)

        async with aiohttp.ClientSession(read_timeout=5, conn_timeout=3) as session:
            async with session.get(url, headers=headers, raise_for_status=True) as response:
                logger.debug(f"Request for {url} status: {response.status}")
                try:
                    result = await response.json()
                except ContentTypeError:
                    result = await response.text()
                return self.__mapping(result)

    async def metrics(self):
        ...


    def get_metric(self, name: str):
        url, headers = self.__prepare_request(name)

        with requests.Session() as session:
            response = session.get(url, headers=headers)
            response.raise_for_status()

            return self.__mapping(response.json())
