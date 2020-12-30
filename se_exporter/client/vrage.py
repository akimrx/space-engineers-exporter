#!/usr/bin/env python3

import asyncio
import base64
import hashlib
import hmac
import logging
import random
from datetime import datetime as dt
from itertools import count
from time import mktime, time
from typing import Dict, List, Optional, Tuple
from wsgiref.handlers import format_date_time

import aiohttp
import requests
from se_exporter.models.base import Base
from se_exporter.utils.helpers import universal_obj_hook

logger = logging.getLogger(__name__)


class Metric(Base):
    """This object represents a SE metric."""
    def __init__(self, name: str = None, **kwargs):
        self.name = name

        for key, value in kwargs.items():
            if isinstance(key, str):
                setattr(self, key, value)


class VRageAPI(Base):
    """Сlient for VRage Remote API.

    Arguments:
      :host: str
      :token: str
      :port: int
      :run_async: bool

    """

    __BASE_RESOURCE__ = "server"
    __OTHER_RESOURCES__ = (
        "session/players",
        "session/planets",
        "session/characters",
        "session/grids",
        "session/asteroids",
        "session/floatingObjects",
        "admin/bannedPlayers",
        "admin/kickedPlayers"
    )

    def __init__(self, host: str, token: str, port: int = 8080, run_async: bool = False):
        if not isinstance(host, str):
            raise ValueError("Host is empty or bad format")
        if token is None:
            raise ValueError("Remote API key can't be empty")

        self.host = self.__verify_host(host)
        self.port = port or 8080
        self.token = token
        self.basepath = "/vrageremote/v1"
        self.endpoint = f"{self.host}:{self.port}{self.basepath}"
        self.nonce = count(int(time() * random.randint(10, 100)))
        self.run_async = run_async
        self.labels = {}
        logger.debug(f"VRageAPI client ready: {self}")

    def __verify_host(self, host: str) -> str:
        if not host.startswith("http://"):
            return f"http://{host}"

    def __date(self) -> str:
        return format_date_time(
            mktime(dt.now().timetuple())
        )

    def __hash(self, uri: str, dtime: str) -> str:
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

    def __prepare_request(self, path: str) -> Tuple:
        if not path.startswith("/"):
            path = f"/{path}"

        dtime = self.__date()
        url = self.endpoint + path

        resource_fullpath = self.basepath + path
        authorization = self.__hash(resource_fullpath, dtime)
        headers = dict(Date=dtime, Authorization=authorization)

        return url, headers

    def __mapping(self, data: dict) -> [Optional[Metric], Optional[List]]:
        if data is None or not isinstance(data, dict):
            return

        players = []
        if len(data) > 1:
            logger.warning(f"Unhandled metrics received, {data}")
            return

        for name, value in data.items():
            if isinstance(value, list):
                if name == "players" and len(value) > 0:
                    for i in value:
                        if i.get("Ping") > 0:
                            players.append(
                                Metric(
                                    name="player_ping",
                                    value=i.get("Ping"),
                                    player_name=i.get("DisplayName"),
                                    player_id=str(i.get("SteamID")),
                                    faction=i.get("FactionName"),
                                    **self.labels
                                )
                            )
                else:
                    value = len(value)
            elif isinstance(value, bool):
                value = int(value)

        if players:
            return players
        return Metric(name=name, value=value, **self.labels)

    async def aioget_metric(self, name: str) -> Dict:
        url, headers = self.__prepare_request(name)

        async with aiohttp.ClientSession(read_timeout=5, conn_timeout=5) as session:
            async with session.get(url, headers=headers, raise_for_status=True) as response:
                logger.debug(f"Request for {url} status: {response.status}")
                try:
                    res = await response.json()
                except Exception as e:
                    logger.error(e)
                    return

            result = res.get("data")
            if name != "server":
                return self.__mapping(universal_obj_hook(result))
            return universal_obj_hook(result)

    def aiofetch_metrics(self) -> List:
        queue = [self.aioget_metric(res) for res in self.__OTHER_RESOURCES__]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        metrics = loop.run_until_complete(asyncio.gather(*queue))
        loop.close()

        rewrited_metrics = []
        for metric in metrics:
            if isinstance(metric, list):
                for m in metric:
                    rewrited_metrics.append(m)
            else:
                rewrited_metrics.append(metric)
        return rewrited_metrics

    def get_metric(self, name: str) -> Dict:
        url, headers = self.__prepare_request(name)

        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=5)
            logger.debug(f"Request for {url} status: {response.status_code}")
            response.raise_for_status()

            result = response.json().get("data")
            if name != "server":
                return self.__mapping(universal_obj_hook(result))
            return universal_obj_hook(result)

    def fetch_metrics(self) -> List:
        metrics = []
        for res in self.__OTHER_RESOURCES__:
            metric = self.get_metric(res)
            if isinstance(metric, list):
                for m in metric:
                    metrics.append(m)
            else:
                metrics.append(metric)
        return metrics

    def metrics(self) -> List:
        """Returns a list of metrics. Each metric is a dict."""
        metrics = []

        if self.run_async:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            base_metrics = loop.run_until_complete(self.aioget_metric(self.__BASE_RESOURCE__))
            loop.close()
        else:
            base_metrics = self.get_metric(self.__BASE_RESOURCE__)

        common_labels = ("server_name", "world_name")
        exclude = ("game", "server_id")
        for k, v in base_metrics.items():
            if k in common_labels:
                self.labels.update({k.strip("_name"): v.lower()})

        for k, v in base_metrics.items():
            if k not in exclude and k not in common_labels:
                metrics.append(self.__mapping({k: v}))

        if self.run_async:
            other_metrics = self.aiofetch_metrics()
        else:
            other_metrics = self.fetch_metrics()

        for m in other_metrics:
            if m not in metrics:
                metrics.append(m)

        return metrics
