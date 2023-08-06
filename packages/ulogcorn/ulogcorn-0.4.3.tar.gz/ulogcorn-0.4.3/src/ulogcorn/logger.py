import logging
import sys
from abc import ABC, abstractmethod

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")  # noqa
        self.error_logger.addHandler(handler)
        self.error_logger.setLevel(self.loglevel)
        self.access_logger = logging.getLogger("gunicorn.access")  # noqa
        self.access_logger.addHandler(handler)
        self.access_logger.setLevel(self.loglevel)


class StandaloneApplication(BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class BaseHandler(ABC):

    def __init__(self, level=logging.DEBUG) -> None:
        super().__init__()
        self.level = level
        self.handler = InterceptHandler()

    @abstractmethod
    def setup(self):
        raise NotImplementedError


class UnifyHandler(BaseHandler):

    def __init__(self, level=logging.DEBUG, modules=None) -> None:
        super().__init__(level)
        if modules is None:
            modules = [
                *logging.root.manager.loggerDict.keys(),  # noqa
                "gunicorn",
                "gunicorn.access",
                "gunicorn.error",
                "gunicorn.wsgi",
                "uvicorn",
                "uvicorn.access",
                "uvicorn.error",
                "uvicorn.asgi"
            ]
        self.modules = modules

    def setup(self):
        logging.root.setLevel(self.level)
        seen = set()
        for name in self.modules:
            if name not in seen:
                seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [self.handler]

        logger.configure(handlers=[{"sink": sys.stdout}])


class UvicornHandler(BaseHandler):

    def __init__(self, level=logging.DEBUG) -> None:
        super().__init__(level)

    def setup(self):
        logging.root.handlers = [self.handler]
        logging.root.setLevel(self.level)

        for name in logging.root.manager.loggerDict.keys():  # noqa
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

        logger.configure(handlers=[{"sink": sys.stdout}])
