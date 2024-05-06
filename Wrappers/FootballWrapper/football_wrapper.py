from typing import Any

from Wrappers.BaseWrapper.base_wrapper import BaseWrapper
from Wrappers.BaseWrapper.base_wrapper_utils import SportKey


class FootballWrapper(BaseWrapper):
    def __init__(self):
        super(SportKey.FOOTBALL)

    def collect_data(self, url: str):
        super().collect_data(url)

    def publish_data(self, data: Any):
        super().publish_data(data)
