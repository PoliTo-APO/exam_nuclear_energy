from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Material(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def energy(self) -> float:
        pass

    @property
    @abstractmethod
    def info(self) -> str:
        pass

    @property
    @abstractmethod
    def auxiliary(self) -> Optional["Material"]:
        pass

    @abstractmethod
    def set_auxiliary(self, material: "Material") -> None:
        pass

    @abstractmethod
    def add_product(self, product: "Material", quantity: float) -> None:
        pass

    @property
    @abstractmethod
    def products(self) -> List[Tuple["Material", float]]:
        pass
