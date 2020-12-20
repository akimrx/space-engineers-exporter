#!/usr/bin/env python3

import hmac
import base64
import hashlib
import asyncio
import aiohttp
import logging

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

        self.host = self._verify_host(host)
        self.port = port
        self.token = token
        self.basepath = "/vrageremote/v1"
        self.endpoint = f"{self.host}:{self.port}{self.basepath}"
        self.nonce = count(int(time()))
        logger.debug(f"VRageAPI client ready: {self}")

    def _verify_host(self, host: str):
        if not host.startswith("http://"):
            return f"http://{host}"

    def _date(self):
        return format_date_time(
            mktime(dt.now().timetuple())
        )

    def _hash(self, uri: str, dtime: str):
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

    def _prepare_request(self, path: str):
        if not path.startswith("/"):
            path = f"/{path}"

        dtime = self._date()
        url = self.endpoint + path

        resource_fullpath = self.basepath + path
        authorization = self._hash(resource_fullpath, dtime)
        headers = dict(Date=dtime, Authorization=authorization)

        return url, headers

    async def get_metric(self, name: str):
        url, headers = self._prepare_request(name)

        async with aiohttp.ClientSession() as session:
            # , raise_for_status=True
            async with session.get(url, headers=headers) as response:
                logger.debug(response.status)
                result = await response.json()
                return result

    async def metrics(self):
        ...

