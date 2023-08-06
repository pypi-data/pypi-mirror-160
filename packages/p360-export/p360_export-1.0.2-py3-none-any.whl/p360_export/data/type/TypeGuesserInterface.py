from abc import ABC, abstractmethod
from typing import Dict


class TypeGuesserInterface(ABC):
    @property
    @abstractmethod
    def type_map(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def guess(self, column_name: str) -> str:
        pass
