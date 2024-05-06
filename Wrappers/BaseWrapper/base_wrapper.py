from abc import ABCMeta, abstractmethod
from typing import Any

from Wrappers.BaseWrapper.base_wrapper_utils import BaseWrapperUtils, SportKey


class BaseWrapper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, exchange: str, sport: SportKey):
        self.exchange = exchange
        self.utils = BaseWrapperUtils(sport)
        self.utils.init_client()
        self.utils.exchange_declare(exchange)

    @abstractmethod
    def collect_data(self, url: str) -> Any:
        pass

    @abstractmethod
    def publish_data(self, data: Any) -> Any:
        pass


# Concrete class implementing BaseWrapper
class Wrapper(BaseWrapper):
    def __init__(self, exchange: str, sport: SportKey):
        super().__init__(exchange, sport)

    def collect_data(self, url: str):
        if url != "":
            collected_data = self.utils.call_api(url)
            return collected_data
        return None

    def publish_data(self, data: Any):
        if data is not None:
            res = self.utils.publish_to(data)
            return res
        return None
