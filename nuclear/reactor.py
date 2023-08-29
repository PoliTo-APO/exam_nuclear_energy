from nuclear.materials import Material, Fuel, Waste, Auxiliary
from typing import Tuple, List, Optional, Set


class ReactorSimulator:
    def __init__(self):
        self._materials = {}

    # R1
    def add_fuel(self, name: str, energy: float, price: int) -> None:
        self._materials[name] = Fuel(name, energy, price)

    def add_waste(self, name: str, energy: float, disposal_cost: int) -> None:
        self._materials[name] = Waste(name, energy, disposal_cost)

    def add_auxiliary(self, name: str) -> None:
        self._materials[name] = Auxiliary(name)

    def get_material(self, name) -> Material:
        return self._materials[name]

    # R3
    def add_intermediate(self, product: str, intermediate: str, quantities: Tuple[float, float]) -> Optional[List[str]]:
        intermediate = self._materials[intermediate]
        product = self._materials[product]
        for material in self._materials.values():
            if product.name in [p.name for p, _ in material.products]:
                material.remove_product(product.name)
                material.add_product(intermediate, quantities[0])
                intermediate.add_product(product, quantities[1])
                return
        
    # R4
    def find_inconsistency(self, fuel: str, auxiliary: Set[str]) -> Optional[str]:
        fuel = self._materials[fuel]
        materials = [fuel]
        inconsistency = None
        while materials and not inconsistency:
            mat = materials.pop()
            if mat.products:
                if mat.auxiliary is not None and mat.auxiliary.name not in auxiliary:
                    inconsistency = mat.auxiliary.name
                else:
                    for mat, _ in mat.products:
                        materials.append(mat)
        return inconsistency

    # R5
    def simulate_reaction(self, fuel, quantity) -> Tuple[List[Tuple[str, float]], float, float]:
        fuel = self._materials[fuel]
        unused = []
        energy, disposal = ReactorSimulator.recursive_sim(fuel, quantity, unused)
        return unused, energy, disposal

    @staticmethod
    def recursive_sim(material, quantity, unused):
        energy = 0
        disposal = 0
        if not material.products:
            unused.append((material.name, quantity))
            disposal = material.disposal_cost * quantity
        else:
            for prod, qt in material.products:
                energy_prod, disposal_prod = ReactorSimulator.recursive_sim(prod, qt*quantity, unused)
                energy += energy_prod
                disposal += disposal_prod
            energy += material.energy * quantity
        return energy, disposal
