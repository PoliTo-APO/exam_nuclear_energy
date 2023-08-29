from nuclear.materials import Material
from typing import Tuple, List, Optional, Set


class ReactorSimulator:
    def __init__(self):
        pass

    # R1
    def add_fuel(self, name: str, energy: float, price: int) -> None:
        pass

    def add_waste(self, name: str, energy: float, disposal_cost: int) -> None:
        pass

    def add_auxiliary(self, name: str) -> None:
        pass

    def get_material(self, name) -> Material:
        pass

    # R3
    def add_intermediate(self, product: str, intermediate: str, quantities: Tuple[float, float]) -> Optional[List[str]]:
        pass
        
    # R4
    def find_inconsistency(self, fuel: str, auxiliary: Set[str]) -> Optional[str]:
        pass

    # R5
    def simulate_reaction(self, fuel, quantity) -> Tuple[List[Tuple[str, float]], float, float]:
        pass
