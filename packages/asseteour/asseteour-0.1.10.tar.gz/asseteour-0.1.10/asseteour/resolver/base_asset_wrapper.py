from abc import ABCMeta, abstractmethod
from typing import Dict


class BaseAssetWrapper(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def parse_obj(cls, payload: Dict):
        pass

    @classmethod
    @abstractmethod
    def schema_json(cls, indent=4):
        pass

    @property
    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def json(self):
        pass

    @abstractmethod
    def yaml(self):
        pass
