import logging
import argparse

from typing import Coroutine

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
commands.add_argument("-p", "--port",  metavar="port", type=int, help="Remote API port. Default: 8080")
commands.add_argument("-t", "--token", metavar="key", type=str, help="Remote API secret key")
commands.add_argument("-c", "--config", metavar="file", type=str, help="Path to the config file")
commands.add_argument("--help", action="help", help="Show help message")

options = parser.add_argument_group("Options")
options.add_argument(
    "-a", "--run-async", action="store_true", help="Enable async collect metrics. \
    If your se server doesn't have good perfomance - don't use this feature"
)
options.add_argument(
    "--loglevel", metavar="debug/info/warning/error", type=str, help="Log facility. Default: info"
)
args = parser.parse_args()
config = Config(args.config)
logging.basicConfig(
    level=args.loglevel or config.LOGLEVEL or "info",
    datefmt="%H:%M:%S",
    format="%(asctime)s – %(levelname)s – %(message)s"
)


def main(host: str, port: int, token: str, run_async: bool = False) -> None:
    try:
        client = VRageAPI(
            host=host,
            port=port,
            token=token
        )
    except Exception as e:
        print("ERROR:", e)
        return

    if run_async:
        client.aiometrics()
    else:
        client.metrics()


if __name__ == "__main__":
    main(
        host=args.host or config.HOST,
        port=args.port or config.PORT,
        token=args.token or config.TOKEN,
        run_async=args.run_async
    )
