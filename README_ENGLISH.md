# Nuclear Fission
Some engineers are finalizing the design of a new nuclear fission power plant and they need software to test the fission process.

The modules and classes should be developed within the *nuclear* package.
Do not move or rename existing modules and classes, and do not modify the method signatures.

The *main.py* file provides some simple code that tests the basic functionalities, which you can modify.
It demonstrates examples of using the main methods and includes the required checks.

Unless otherwise specified, all exceptions are of type *ReactorException* defined in the *errors* module.


## R1: Materials (5/21)
The abstract class *Material* in the *materials* module represents a material that participates in nuclear fission.
It defines the following abstract properties:
- ```name(self) -> str```
- ```energy(self) -> float```
- ```info(self) -> str```

These properties provide the name, the energy produced by the fission of **ONE GRAM** of the material, and other material-specific information.

The class *ReactorSimulator* in the *nuclear* module allows the addition of different types of materials.

The method
```add_fuel(self, name: str, energy: float, price: int) -> None```
is used to define a new fuel for fission by specifying its name, the energy produced by fission of **ONE GRAM**, and the price per gram.

The method
```add_waste(self, name: str, energy: float, disposal_cost: int) -> None```
is used to add nuclear waste by specifying its name, the energy produced the fission of **ONE GRAM**,
and the cost of disposal of **ONE GRAM**.

The method
```add_auxiliary(self, name: str) -> None```
is used to add an auxiliary material by specifying its name.
The ```energy(self) -> float``` property for an auxiliary material always returns 0.

The method
```get_material(self, name: str) -> Material```
allows retrieving the object representing a material by providing its name.

The ```info(self) -> str``` property returns the material's information. For a fuel, it returns its price preceded by the word *Price* and separated by a space. For waste, it returns the word *Disposal* followed by the disposal cost, separated by a space.
Examples:
- *Price 22*
- *Disposal 5*

For an auxiliary material, the ```info(self) -> str``` property returns an empty string.


## R2: Reaction (5/21)
The abstract class *Material* has additional abstract methods used to define the fission process.
The fission process starts with a material (usually a fuel) that splits into various fuels and waste.
The produced fuels and waste further split until they reach non-decomposable fuels or waste.

The method ```add_product(self, product: "Material", quantity: float) -> None``` is used to add a fission product of a material,
which means a material in which the original material decomposes during the reaction.
The second parameter specifies the grams of product generated per gram of the original material.
If the method is called on an auxiliary material, an exception is thrown.

The ```products(self) -> List[Tuple["Material", float]]``` property returns a list containing tuples for each fission product.
Each tuple contains the object representing the generated material and the respective quantity in grams produced per gram of the original material.
For **ALL** types of materials on which the method is executed, including auxiliaries, if there are no fission products, the method should return an empty list.

The ```set_auxiliary(self, material: "Material") -> None``` method allows setting an auxiliary material necessary for the fission reaction of the material.
The method throws an exception if called on an auxiliary material.

The ```auxiliary(self) -> Optional["Material"]``` property allows obtaining the auxiliary material of another material.
For **ALL** types of materials on which the method is executed, including auxiliaries, if there is no auxiliary material, it should return ```None```.

**IMPORTANT:** Assume that the fission process structure is a tree, where each waste or fuel can appear at most once.


## R3: Intermediate Products (3/21)
The method ```add_intermediate(self, product: str, intermediate: str, quantities: Tuple[float, float]) -> Optional[List[str]]``` in *ReactorSimulator* allows adding an intermediate product before a fission product.
The name of the fission product that should be preceded by the intermediate product is provided as the first parameter.
The name of the intermediate product to add is provided as the second parameter.

For example, if the material *mat* produced the product *prod*, now the material *mat* should produce the intermediate product *int*, and the intermediate product *int* will, in turn, produce the product *prod*.

The quantities in grams of the intermediate product per gram of the original material, and the quantities in grams of the product given the quantities of the intermediate product, are provided as a tuple through the third parameter.

**ATTENTION**: Since the fission process has a tree structure, each material has at most one parent.

## R4: Inconsistency Analysis (4/21)
The method ```find_inconsistency(self, fuel: str, auxiliary: Set[str]) -> Optional[str]``` in *ReactorSimulator* accepts the name of a fuel and a set of names of auxiliary materials introduced in the reactor as parameters.
The method simulates the reaction until non-decomposable materials are reached and checks if, for each decomposing material, its auxiliary material, **WHEN REQUIRED**, is among those introduced in the reactor.
If a missing auxiliary material is found, the method returns its name; otherwise, it returns ```None```.

**IMPORTANT:** Assume that at most one missing auxiliary material exists.

## R5: Simulation (4/21)
The method ```simulate_reaction(self, fuel, quantity) -> Tuple[List[Tuple[str, float]], float, float]``` in *ReactorSimulator* allows simulating the outcome of a reaction.
The method accepts the name of a fuel and its quantity in grams as parameters.
The method should simulate the reaction, assuming that auxiliary materials are always available, until non-decomposable materials are obtained.

**NOTE:** Assume that the non-decomposable materials are *ALWAYS* waste.

The method should return a tuple consisting of three elements:
- a list of tuples, each containing the name of a non-decomposable waste and its quantity.
- the total energy produced by all decomposing elements.
- the disposal cost of all non-decomposable wastes.

**NOTE:** Remember that the energy and disposal cost depend on the quantity of the material.