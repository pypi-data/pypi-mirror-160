import sys

import uvicorn
from loguru import logger
from ulogcorn import UvicornHandler
from uvicorn import Server
from uvicorn.supervisors import ChangeReload, Multiprocess


class Config(uvicorn.Config):
    def configure_logging(self):
        super().configure_logging()
        UvicornHandler().setup()


def run(app, **kwargs):
    config = Config(app, **kwargs)
    server = Server(config=config)

    if (config.reload or config.workers > 1) and not isinstance(app, str):
        logger.warning("You must pass the application as an import string to enable 'reload' or  'workers'.")
        sys.exit(1)

    if config.should_reload:
        sock = config.bind_socket()
        supervisor = ChangeReload(config, target=server.run, sockets=[sock])
        supervisor.run()
    elif config.workers > 1:
        sock = config.bind_socket()
        supervisor = Multiprocess(config, target=server.run, sockets=[sock])
        supervisor.run()
    else:
        server.run()
