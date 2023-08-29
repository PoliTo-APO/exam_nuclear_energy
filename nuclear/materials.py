from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from nuclear.errors import ReactorException


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


class NuclearMaterial(Material):
    def __init__(self, name, energy):
        self._name = name
        self._energy = energy
        self._products = []
        self._auxiliary = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def info(self) -> str:
        return ""

    @property
    def auxiliary(self):
        return self._auxiliary

    def set_auxiliary(self, material):
        self._auxiliary = material

    def add_product(self, product, quantity):
        self._products.append((product, quantity))

    @property
    def products(self):
        return self._products    

    def remove_product(self, product):
        self._products = [(prod, qt) for prod, qt in self._products if prod.name != product]


class Fuel(NuclearMaterial):
    def __init__(self, name, energy, price):
        super().__init__(name, energy)
        self._price = price

    @property
    def price(self) -> int:
        return self._price

    @property
    def info(self) -> str:
        return "Price {}".format(self.price)


class Waste(NuclearMaterial):
    def __init__(self, name, energy, disposal_cost):
        super().__init__(name, energy)
        self._disposal_cost = disposal_cost

    @property
    def disposal_cost(self) -> int:
        return self._disposal_cost

    @property
    def info(self) -> str:
        return "Disposal {}".format(self.disposal_cost)


class Auxiliary(NuclearMaterial):
    def __init__(self, name):
        super().__init__(name, 0)

    def add_product(self, product, quantity):
        raise ReactorException("Auxiliary has no products")

    def set_auxiliary(self, material):
        raise ReactorException("Auxiliary cannot have auxiliary")
    

