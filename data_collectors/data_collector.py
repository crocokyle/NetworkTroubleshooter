# Local imports
from utils.credentials import Credential

# 3rd party imports
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class DataCollector(ABC):
    def __init__(self):
        self.last_run = datetime.fromtimestamp(0)
        self.data: Any = None
        self.target: str = ""
        self.credentials: Credential = None

    @abstractmethod
    def run(self):
        """
        Should gather and store `self.data` and `self.last_run`
        """
        self.last_run = datetime.now()

    def clear(self):
        self.data = None

