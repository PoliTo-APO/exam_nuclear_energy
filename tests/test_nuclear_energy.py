import unittest
from nuclear.materials import Material
from nuclear.reactor import ReactorSimulator
from nuclear.errors import ReactorException


class TestR0(unittest.TestCase):
    
    def test_abstract(self):
        self.assertRaises(TypeError, Material)


class TestR1(unittest.TestCase):

    def setUp(self):
        self._rs = ReactorSimulator()

    def test_add_material(self):
        self._rs.add_fuel("Fuel1", 123.4, 11)
        self._rs.add_waste("Waste1", 11.7, 12)
        self._rs.add_auxiliary("Aux1")
        self.assertEqual("Fuel1", self._rs.get_material("Fuel1").name)
        self.assertEqual("Waste1", self._rs.get_material("Waste1").name)
        self.assertEqual("Aux1", self._rs.get_material("Aux1").name)

    def test_add_properties(self):
        self._rs.add_fuel("Fuel1", 123.4, 11)
        self._rs.add_waste("Waste1", 11.7, 12)
        self._rs.add_auxiliary("Aux1")

        self.assertAlmostEqual(123.4, self._rs.get_material("Fuel1").energy)        
        self.assertAlmostEqual(11.7, self._rs.get_material("Waste1").energy)
        self.assertAlmostEqual(0, self._rs.get_material("Aux1").energy)

    def test_info(self):
        self._rs.add_fuel("Fuel1", 123.4, 11)
        self._rs.add_waste("Waste1", 11.7, 12)
        self._rs.add_auxiliary("Aux1")

        fuel = self._rs.get_material("Fuel1")
        waste = self._rs.get_material("Waste1")
        aux = self._rs.get_material("Aux1")

        self.assertTrue("Price" in fuel.info)
        self.assertTrue("11" in fuel.info)
        self.assertTrue("Disposal" in waste.info)
        self.assertTrue("12" in waste.info)
        self.assertEqual("", aux.info)

    def test_add_multiple(self):
        self._rs.add_fuel("Fuel1", 1, 2)
        self._rs.add_waste("Waste1", 3, 4)
        self._rs.add_auxiliary("Aux1")

        self._rs.add_fuel("Fuel2", 5, 6)    
        self._rs.add_waste("Waste2", 7, 8)
        self._rs.add_auxiliary("Aux2")

        self.assertEqual("Fuel1", self._rs.get_material("Fuel1").name)
        self.assertEqual("Waste1", self._rs.get_material("Waste1").name)
        self.assertEqual("Aux1", self._rs.get_material("Aux1").name)

        self.assertEqual("Fuel2", self._rs.get_material("Fuel2").name)
        self.assertEqual("Waste2", self._rs.get_material("Waste2").name)
        self.assertEqual("Aux2", self._rs.get_material("Aux2").name)

    def test_add_multiple_properties(self):
        self._rs.add_fuel("Fuel1", 1, 2)
        self._rs.add_waste("Waste1", 3, 4)
        self._rs.add_auxiliary("Aux1")

        self._rs.add_fuel("Fuel2", 5, 6)    
        self._rs.add_waste("Waste2", 7, 8)
        self._rs.add_auxiliary("Aux2")

        self.assertAlmostEqual(1, self._rs.get_material("Fuel1").energy)        
        self.assertAlmostEqual(3, self._rs.get_material("Waste1").energy)
        self.assertAlmostEqual(0, self._rs.get_material("Aux1").energy)

        self.assertAlmostEqual(5, self._rs.get_material("Fuel2").energy)        
        self.assertAlmostEqual(7, self._rs.get_material("Waste2").energy)
        self.assertAlmostEqual(0, self._rs.get_material("Aux2").energy)


class TestR2(unittest.TestCase):

    def setUp(self):
        self._rs = ReactorSimulator()
        self._rs.add_fuel("Fuel1", 1, 2)
        self._rs.add_waste("Waste1", 3, 4)
        self._rs.add_auxiliary("Aux1")

        self._rs.add_fuel("Fuel2", 5, 6)    
        self._rs.add_waste("Waste2", 7, 8)
        self._rs.add_auxiliary("Aux2")

    def test_set_auxiliary(self):
        fuel1 = self._rs.get_material("Fuel1")
        aux1 = self._rs.get_material("Aux1")
        fuel2 = self._rs.get_material("Fuel2")
        aux2 = self._rs.get_material("Aux2")
        waste2 = self._rs.get_material("Waste2")

        fuel1.set_auxiliary(aux1)
        waste2.set_auxiliary(aux2)

        self.assertEqual("Aux1", fuel1.auxiliary.name)
        self.assertEqual("Aux2", waste2.auxiliary.name)
        self.assertIsNone(fuel2.auxiliary)

    def test_auxiliary_exceptions(self):
        aux1 = self._rs.get_material("Aux1")
        aux2 = self._rs.get_material("Aux2")
        fuel1 = self._rs.get_material("Fuel1")

        self.assertRaises(ReactorException, aux1.set_auxiliary, aux2)
        self.assertRaises(ReactorException, aux2.add_product, fuel1, 0.2)
    
    def test_add_products(self):
        fuel1 = self._rs.get_material("Fuel1")
        fuel2 = self._rs.get_material("Fuel2")
        waste1 = self._rs.get_material("Waste1")
        waste2 = self._rs.get_material("Waste2")
        
        fuel1.add_product(fuel2, 0.5)
        fuel1.add_product(waste1, 0.2)
        fuel1.add_product(waste2, 0.2)

        products = sorted([prod[0].name for prod in fuel1.products])
        self.assertEqual(["Fuel2", "Waste1", "Waste2"], products)
        self.assertEqual([], waste1.products)

    def test_product_quantities(self):
        fuel1 = self._rs.get_material("Fuel1")
        fuel2 = self._rs.get_material("Fuel2")
        waste1 = self._rs.get_material("Waste1")
        waste2 = self._rs.get_material("Waste2")
        
        fuel1.add_product(fuel2, 0.5)
        fuel1.add_product(waste1, 0.2)
        fuel1.add_product(waste2, 0.1)

        products = sorted([prod[1] for prod in fuel1.products])
        self.assertAlmostEqual(0.1, products[0])
        self.assertAlmostEqual(0.2, products[1])
        self.assertAlmostEqual(0.5, products[2])

    def test_add_products_multiple(self):
        fuel1 = self._rs.get_material("Fuel1")
        fuel2 = self._rs.get_material("Fuel2")
        waste1 = self._rs.get_material("Waste1")
        waste2 = self._rs.get_material("Waste2")
        
        fuel1.add_product(waste1, 0.5)
        fuel2.add_product(waste2, 0.2)

        self.assertEqual(1, len(fuel1.products))
        self.assertEqual(1, len(fuel2.products))

        self.assertEqual("Waste1", fuel1.products[0][0].name)
        self.assertAlmostEqual(0.5, fuel1.products[0][1])
        self.assertEqual("Waste2", fuel2.products[0][0].name)
        self.assertAlmostEqual(0.2, fuel2.products[0][1])


class TestR3(unittest.TestCase):

    def setUp(self):
        self._rs = ReactorSimulator()
        self._rs.add_fuel("Fuel1", 1, 2)
        self._rs.add_waste("Waste1", 3, 4)
        self._rs.add_fuel("Fuel2", 5, 6)    
        self._rs.add_waste("Waste2", 7, 8)
        self._rs.add_waste("Waste3", 9, 10)

        fuel1 = self._rs.get_material("Fuel1")
        fuel2 = self._rs.get_material("Fuel2")
        waste1 = self._rs.get_material("Waste1")
        waste2 = self._rs.get_material("Waste2")
        waste3 = self._rs.get_material("Waste3")
        
        fuel1.add_product(fuel2, 0.5)
        fuel1.add_product(waste1, 0.2)
        fuel1.add_product(waste2, 0.2)

    def test_intermediate_after(self):
        self._rs.add_intermediate("Fuel2", "Waste3", (0.4, 0.7))
        prod, qt = self._rs.get_material("Waste3").products[0]
        self.assertEqual("Fuel2", prod.name)

    def test_intermediate_before(self):
        self._rs.add_intermediate("Fuel2", "Waste3", (0.4, 0.7))
        products = sorted(self._rs.get_material("Fuel1").products, key=lambda x: x[0].name)

        self.assertEqual("Waste1", products[0][0].name)
        self.assertEqual("Waste2", products[1][0].name)
        self.assertEqual("Waste3", products[2][0].name)

    def test_intermediate_quantities(self):
        self._rs.add_intermediate("Fuel2", "Waste3", (0.4, 0.7))
        prod, qt = self._rs.get_material("Waste3").products[0]        
        self.assertAlmostEqual(0.7, qt)
        prod, qt = [(prod, qt) for prod, qt in self._rs.get_material("Fuel1").products if prod.name == "Waste3"][0]       
        self.assertAlmostEqual(0.4, qt)


class TestR4(unittest.TestCase):

    def setUp(self) -> None:
        self._rs = ReactorSimulator()
        self._rs.add_fuel("Fuel1", 1, 2)
        self._rs.add_fuel("Fuel2", 5, 6) 
        self._rs.add_waste("Waste1", 3, 4)           
        self._rs.add_waste("Waste2", 7, 8)
        self._rs.add_waste("Waste3", 9, 10)
        self._rs.add_auxiliary("Aux1")
        self._rs.add_auxiliary("Aux2")
        self._rs.add_auxiliary("Aux3")
        self._rs.add_auxiliary("Aux4")
        self._rs.add_auxiliary("Aux5")

        self._fuel1 = self._rs.get_material("Fuel1")
        self._fuel2 = self._rs.get_material("Fuel2")
        self._waste1 = self._rs.get_material("Waste1")
        self._waste2 = self._rs.get_material("Waste2")
        self._waste3 = self._rs.get_material("Waste3")
        self._aux1 = self._rs.get_material("Aux1")
        self._aux2 = self._rs.get_material("Aux2")
        self._aux3 = self._rs.get_material("Aux3")
        self._aux4 = self._rs.get_material("Aux4")
        self._aux5 = self._rs.get_material("Aux5")

    def test_inconsistency_start(self):
        self._fuel1.set_auxiliary(self._aux1)
        self._fuel2.set_auxiliary(self._aux2)
        self._waste3.set_auxiliary(self._aux3)

        self._fuel1.add_product(self._fuel2, 1)
        self._fuel2.add_product(self._waste1, 2)

        self.assertEqual("Aux1", self._rs.find_inconsistency("Fuel1", {"Aux2", "Aux3"}))

    def test_inconsistency_complex(self):
        self._fuel1.set_auxiliary(self._aux1)
        self._fuel2.set_auxiliary(self._aux2)
        self._waste3.set_auxiliary(self._aux3)
        self._waste1.set_auxiliary(self._aux4)
        self._waste2.set_auxiliary(self._aux5)

        self._fuel1.add_product(self._fuel2, 1)
        self._fuel1.add_product(self._waste1, 2)
        self._fuel2.add_product(self._waste2, 3)
        self._waste1.add_product(self._waste3, 4)

        self.assertEqual("Aux4", self._rs.find_inconsistency("Fuel1", {"Aux1", "Aux2", "Aux3", "Aux5"}))

    def test_inconsistency_complex_missing(self):
        self._fuel1.set_auxiliary(self._aux1)
        self._fuel2.set_auxiliary(self._aux2)
        self._waste3.set_auxiliary(self._aux3)

        self._fuel1.add_product(self._fuel2, 1)
        self._fuel1.add_product(self._waste1, 2)
        self._fuel2.add_product(self._waste2, 3)
        self._waste1.add_product(self._waste3, 4)

        self.assertEqual("Aux2", self._rs.find_inconsistency("Fuel1", {"Aux1", "Aux3", "Aux4", "Aux5"}))

    def test_inconsistency_none(self):
        self._fuel1.set_auxiliary(self._aux1)
        self._fuel2.set_auxiliary(self._aux2)
        self._waste3.set_auxiliary(self._aux3)

        self._fuel1.add_product(self._fuel2, 1)
        self._fuel2.add_product(self._waste1, 2)

        self.assertEqual("Aux2", self._rs.find_inconsistency("Fuel1", {"Aux1", "Aux3"}))
        self.assertIsNone(self._rs.find_inconsistency("Fuel1", {"Aux1", "Aux2", "Aux3"}))


class TestR5(unittest.TestCase):

    def setUp(self) -> None:
        self._rs = ReactorSimulator()
        self._rs.add_fuel("Fuel1", 10, 1)
        self._rs.add_fuel("Fuel2", 9, 1)
        self._rs.add_fuel("Fuel3", 8, 1)
        self._rs.add_waste("Waste1", 1, 7)        
        self._rs.add_waste("Waste2", 1, 6)
        self._rs.add_waste("Waste3", 1, 5)
        self._rs.add_waste("Waste4", 1, 4)

        fuel1 = self._rs.get_material("Fuel1")
        fuel2 = self._rs.get_material("Fuel2")
        fuel3 = self._rs.get_material("Fuel3")
        waste1 = self._rs.get_material("Waste1")
        waste2 = self._rs.get_material("Waste2")
        waste3 = self._rs.get_material("Waste3")
        
        fuel1.add_product(fuel2, 0.5)
        fuel1.add_product(waste1, 0.4)
        fuel1.add_product(fuel3, 0.1)
        fuel2.add_product(waste3, 0.6)
        fuel3.add_product(waste2, 0.7)

    def test_simulation_waste(self):
        residual, _, _ = self._rs.simulate_reaction("Fuel1", 32.5)
        waste = [name for name, qt in residual]
        self.assertEqual(3, len(waste))
        self.assertEqual({"Waste1", "Waste2", "Waste3"}, set(waste))

    def test_simulation_quantities(self):
        residual, _, _ = self._rs.simulate_reaction("Fuel1", 32.5)
        quantities = [qt for name, qt in sorted(residual, key=lambda x: x[0])]
        self.assertAlmostEqual(32.5*0.4, quantities[0])
        self.assertAlmostEqual(32.5*0.1*0.7, quantities[1])
        self.assertAlmostEqual(32.5*0.5*0.6, quantities[2])

    def test_simulation_energy(self):
        _, energy, _ = self._rs.simulate_reaction("Fuel1", 32.5)
        self.assertAlmostEqual(32.5*10 + 32.5*0.5*9 + 32.5*0.1*8, energy)

    def test_simulation_disposal(self):
        _, _, disposal = self._rs.simulate_reaction("Fuel1", 32.5)
        self.assertAlmostEqual(32.5*0.4*7 + 32.5*0.1*0.7*6 + 32.5*0.5*0.6*5, disposal)
    