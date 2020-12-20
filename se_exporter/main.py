import asyncio
import logging

from utils.config import Config
from client.vrage import VRageAPI

config = Config("./config.yaml")

logging.basicConfig(level=logging.DEBUG)

RESOURCES = (
    # "session/players",
    # "session/planets",
    # "session/characters",
    # "session/grids",
    # "session/asteroids",
    # "session/floatingObjects",
    "server",
    # "admin/bannedPlayers",
    # "admin/kickedPlayers"
)


def main():
    vrage = VRageAPI(
        host=config.HOST,
        port=config.PORT,
        token=config.TOKEN
    )

    tasks = [vrage.get_metric(res) for res in RESOURCES]
    return asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    metrics = loop.run_until_complete(main())
    for metric in metrics:
        print(metric)

    loop.close()
