from abc import ABC, abstractmethod


class Provider(ABC):
    @staticmethod
    @abstractmethod
    def provide_data(**kwargs):
        pass

    @staticmethod
    @abstractmethod
    def use(**kwargs):
        pass
