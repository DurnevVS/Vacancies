from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get(self):
        ...
