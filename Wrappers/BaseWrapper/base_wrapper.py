import requests
from abc import ABCMeta, abstractmethod
from Wrappers.BaseWrapper.base_wrapper_utils import BaseWrapperUtils


class BaseWrapper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, exchange: str, url: str):
        self.utils = BaseWrapperUtils()

        # Connection to RabbitMQ
        self.exchange = exchange
        self.utils.init_client()
        self.utils.publish_to(exchange)

        # Connection to API
        self.url = url

    @abstractmethod
    def collect_data(self):
        pass
