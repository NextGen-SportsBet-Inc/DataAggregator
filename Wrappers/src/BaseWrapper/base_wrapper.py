from abc import ABCMeta, abstractmethod
from typing import Any
from BaseWrapper.base_wrapper_utils import BaseWrapperUtils, SportKey


class BaseWrapper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, exchange: str, sport: SportKey) -> None:
        self.exchange = exchange
        self.utils = BaseWrapperUtils(sport)
        self.utils.init_client()
        self.utils.exchange_declare(exchange)
    
    @abstractmethod
    def declare_queue(self, queue: str, routing_key: str) -> None:
        pass
        
    @abstractmethod
    def collect_data(self, url: str) -> Any:
        pass

    @abstractmethod
    def publish_data(self, data: Any, routing_key: str = '') -> Any:
        pass


# Concrete class implementing BaseWrapper
class Wrapper(BaseWrapper):
    def __init__(self, exchange: str, sport: SportKey):
        super().__init__(exchange, sport)
        
    def declare_queue(self, queue: str, routing_key: str):
        self.utils.declare_queue(queue, routing_key)

    def collect_data(self, url: str):
        if url != "":
            collected_data = self.utils.call_api(url)
            return collected_data
        return None

    def publish_data(self, data: Any, routing_key: str = ''):
        if data is not None:
            res = self.utils.publish_to(data, routing_key)
            return res
        return None
