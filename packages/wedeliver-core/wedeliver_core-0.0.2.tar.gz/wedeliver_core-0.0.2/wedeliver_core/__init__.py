# from flask import current_app, _app_ctx_stack

from .app_decorators.app_entry import route
from .helpers.log_config import init_logger
from .helpers.config import Config
from .helpers.kafka_producer import Producer
from .helpers.topics import Topics
from .helpers.micro_fetcher import MicroFetcher


class WeDeliverCore:
    __app = None

    @staticmethod
    def getApp():
        """ Static access method. """
        if WeDeliverCore.__app == None:
            WeDeliverCore()
        return WeDeliverCore.__app

    def __init__(self, app=None):
        """ Virtually private constructor. """
        if WeDeliverCore.__app != None:
            raise Exception("This class is a singleton!")
        else:
            WeDeliverCore.__app = app


__all__ = [
    "WeDeliverCore",
    "route",
    "Config",
    "Producer",
    "init_logger",
    "Topics",
    "MicroFetcher",
]
