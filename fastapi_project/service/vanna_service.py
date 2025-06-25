from abc import ABC, abstractmethod
from fastapi import UploadFile


class VannaService(ABC):
    @abstractmethod
    def ask_vanna(self,query:str):
        pass