
import glob
import os
import random
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from enum import Enum


class AbstractAssetBuilder(metaclass=ABCMeta):

    @abstractmethod
    def build(self):
        """Build assets with the assigned config.
        """
        pass

    @abstractmethod
    def pre_build(self):
        """Implement the behaviors to prepare the data before creating new assets.
        """
        pass

    @abstractmethod
    def post_build(self):
        """Implement the behaviors to response the build results.
        """
        pass

    @abstractmethod
    def load_cache(self):
        """Implement the behaviors to response the build results.
        """
        pass

    @abstractmethod
    def run(self, cache: bool = False):
        """Build assets with the given skin ID.
        """
        pass

    @abstractmethod
    def validator(self):
        """Invlove the function to validate assets.
        """
        pass

    @abstractmethod
    def export_cache(self):
        pass


class AssetBuilder(AbstractAssetBuilder):
    def __init__(self, config):
        pass

    def validator(self):
        pass

    def build(self):
        pass

    def load_cache(self):
        pass

    def pre_build(self):
        pass

    def post_build(self):
        pass

    def run(self, cache: bool = False):

        self.pre_build()

        self.validator()

        if cache:
            self.load_cache()
        else:
            self.build()

        return self.post_build()

    def export_cache(self):
        pass
