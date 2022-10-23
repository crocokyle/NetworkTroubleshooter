# Local imports
from utils.credentials import Credential
from utils.data_structures import Data, Fact
from utils.network import Endpoint

# 3rd party imports
from abc import ABC, abstractmethod
from datetime import datetime


class DataCollector(ABC):
    def __init__(self):
        self.last_run = datetime.fromtimestamp(0)
        self.data: Data[Fact] = Data()
        self.target: str = ""
        self.credentials: Credential = None
        self.endpoints: list[Endpoint] = []

    @abstractmethod
    def run(self) -> None:
        """
        Run any DataCollector methods to gather data.
        Should gather and store `self.data` and `self.last_run`
        Base class returns self.data
        """
        self.last_run = datetime.now()
        return self.data

    def clear(self):
        self.data = None

