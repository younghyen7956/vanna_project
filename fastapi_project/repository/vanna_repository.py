from abc import ABC, abstractmethod

class vannaRepository(ABC):

    @abstractmethod
    def get_DB_openai(self):
        pass

    @abstractmethod
    def ask(self, query:str):
        pass