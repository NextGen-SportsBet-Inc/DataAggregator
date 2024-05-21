from typing import Any

from Wrappers.src.BaseWrapper.base_wrapper import Wrapper
from Wrappers.src.BaseWrapper.base_wrapper_utils import SportKey


class FootballWrapper(Wrapper):
    def __init__(self):
        super().__init__("collected_data/football", SportKey.FOOTBALL)
        
    def declare_queue(self, queue: str, routing_key: str):
        return super().declare_queue(queue, routing_key)

    def collect_data(self, url: str):
        return super().collect_data(url)

    def publish_data(self, data: Any, routing_key: str = ''):
        return super().publish_data(data, routing_key)
