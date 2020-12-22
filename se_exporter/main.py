#!/usr/bin/env python3

import sys
import argparse
import logging

from .__version__ import __version__
from .client.prometheus import SpaceEngineersExporter
from .client.vrage import VRageAPI
from .utils.config import Config

parser = argparse.ArgumentParser(
    prog="space-engineers-exporter",
    description="Prometheus exporter for Space Engineers Dedicated Server",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=90),
    add_help=False
)

# Commands
commands = parser.add_argument_group("Arguments")
commands.add_argument(
    "-h", "--host",
    metavar="host",
    dest="host",
    type=str,
    required=False,
    help="Space Engineers Server (API) host"
)
commands.add_argument(
    "-p", "--port",
    metavar="port",
    dest="port",
    type=int,
    required=False,
    help="SE Remote API port. Default: 8080"
)
commands.add_argument(
    "-t", "--token",
    metavar="key",
    dest="token",
    type=str,
    required=False,
    help="SE Remote API secret key")
commands.add_argument(
    "--listen-addr",
    metavar="addr",
    dest="listen_addr",
    type=str,
    required=False,
    help="Address on which to expose metrics. Default: 0.0.0.0"
)
commands.add_argument(
    "--listen-port",
    metavar="port",
    dest="listen_port",
    type=int,
    required=False,
    help="Port on which to expose metrics. Default: 9122"
)
commands.add_argument(
    "--help",
    action="help",
    help="Show this help message"
)
commands.add_argument(
    "--version",
    action="version",
    version=f"v{__version__}",
    help="Show exporter version"
)

# Options
options = parser.add_argument_group("Options")
options.add_argument(
    "-c", "--config",
    metavar="file",
    type=str,
    required=False,
    help="Path to the config file"
)
options.add_argument(
    "-a", "--run-async",
    action="store_true",
    help="Enable async collect metrics from SE. It works much faster. \
          If your se server doesn't have good perfomance - don't use this feature"
)
options.add_argument(
    "--loglevel",
    metavar="debug/info/warning/error",
    type=str,
    help="Log facility. Default: info"
)

args = parser.parse_args()
config = Config(args.config)

logging.basicConfig(
    level=args.loglevel or config.loglevel,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    client = VRageAPI(
        host=args.host or config.host,
        token=args.token or config.token,
        port=args.port or config.port,
        run_async=args.run_async or config.run_async
    )

    exporter = SpaceEngineersExporter(vrage_client=client)
    exporter.run(
        addr=args.listen_addr or config.listen_addr,
        port=args.listen_port or config.listen_port
    )


if __name__ == "__main__":
    main()
