import asyncio
import logging
import argparse

from utils.config import Config
from client.vrage import VRageAPI

parser = argparse.ArgumentParser(
    prog="space-engineers-exporter",
    description="Prometheus exporter for Space Engineers Dedicated Server",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=90),
    add_help=False
)

commands = parser.add_argument_group("Arguments")
commands.add_argument("-h", "--host", metavar="host", type=str, help="Space Engineers Server host")
commands.add_argument("-p", "--port",  metavar="port", type=int, help="Remote API port")
commands.add_argument("-t", "--token", metavar="key", type=str, help="Remote API secret key")
commands.add_argument("-c", "--config", metavar="file", type=str, help="Path to the config file")
commands.add_argument("--help", action="help", help="Show help message")

options = parser.add_argument_group("Options")
options.add_argument("-a", "--async", action="store_true", help="Enable async collect metrics. \
    if your server doesn't have good perfomance - don't use this feature")
options.add_argument("--loglevel", metavar="debug/info/warning/error", type=str, help="Log facility")
args = parser.parse_args()

config = Config(args.config)
logging.basicConfig(
    level=args.loglevel or config.LOGLEVEL or "info",
    datefmt="%H:%M:%S",
    format="%(asctime)s – %(levelname)s – %(message)s"
)

RESOURCES = (
    "session/players",
    "session/planets",
    "session/characters",
    "session/grids",
    "session/asteroids",
    "session/floatingObjects",
    "server",
    # "admin/bannedPlayers",
    # "admin/kickedPlayers"
)

vrage = VRageAPI(
    host=args.host or config.HOST,
    port=args.port or config.PORT,
    token=args.token or config.TOKEN
)


def async_metrics():
    tasks = [vrage.get_metric(res) for res in RESOURCES]
    return asyncio.gather(*tasks)


def async_serve():
    loop = asyncio.get_event_loop()
    metrics = loop.run_until_complete(async_metrics())
    for metric in metrics:
        print(metric)
    loop.close()


def serve():
    metrics = []
    for res in RESOURCES:
        metrics.append(
            vrage.get_metric(res)
        )

    for metric in metrics:
        print(metric)


# if __name__ == "__main__":
#     serve()
