from nuclear.reactor import ReactorSimulator
from nuclear.errors import ReactorException


def main():
    print("------------------------- R1 -------------------------")
    rs = ReactorSimulator()
    rs.add_fuel("Uranium-235", 11.3, 100)
    rs.add_waste("Bario", 2.5, 50)
    rs.add_auxiliary("Auxiliary1")

    u_235 = rs.get_material("Uranium-235")
    bario = rs.get_material("Bario")
    aux1 = rs.get_material("Auxiliary1")

    print([u_235.name, u_235.energy, u_235.info])   # ['Uranium-235', 11.3, 'Price 100']
    print([bario.name, bario.energy, bario.info])   # ['Bario', 2.5, 'Disposal 50']
    print([aux1.name, aux1.energy, aux1.info])      # ['Auxiliary1', 0, '']

    print("------------------------- R2 -------------------------")
    u_235.set_auxiliary(aux1)
    print(u_235.auxiliary.name)  # Auxiliary1
    
    rs.add_waste("Krypton", 3.2, 40)
    krypton = rs.get_material("Krypton")
    rs.add_auxiliary("Auxiliary2")
    aux2 = rs.get_material("Auxiliary2")

    u_235.add_product(bario, 0.7)
    u_235.add_product(krypton, 0.2)

    # --- STRUCTURE ---
    #  u_235(aux1) -> bario
    #              -> krypton

    print([(prod.name, qt) for prod, qt in u_235.products])  # [('Bario', 0.7), ('Krypton', 0.2)]
    print(bario.products)                                    # []

    try:
        aux1.add_product(bario, 0.3)
        print("[ERROR]: Product added to auxiliary not detected")
    except ReactorException:
        print("Product added to auxiliary correctly detected")  # Product added to auxiliary correctly detected

    try:
        aux1.set_auxiliary(aux2)
        print("[ERROR]: Auxiliary set for auxiliary not detected")
    except ReactorException:
        print("Auxiliary set for auxiliary correctly detected")  # Auxiliary set for auxiliary correctly detected

    print("------------------------- R3 -------------------------")
    rs.add_fuel("Uranium-232", 5.4, 70)
    u_232 = rs.get_material("Uranium-232")
    rs.add_intermediate("Bario", "Uranium-232", (0.3,  0.5))

    # --- STRUCTURE ---
    #  u_235(aux1) -> u_232 -> bario
    #              -> krypton

    print([(m.name, qt) for m, qt in u_235.products])   # [('Krypton', 0.2), ('Uranium-232', 0.3)]
    print([(m.name, qt) for m, qt in u_232.products])   # [('Bario', 0.5)]

    print("------------------------- R4 -------------------------")

    # --- STRUCTURE ---
    # u_235(aux1) -> u_232 -> bario
    #             -> krypton

    print(rs.find_inconsistency("Uranium-235", {"Auxiliary1"}))
    u_232.set_auxiliary(aux2)   # None

    # --- STRUCTURE ---
    # u_235(aux1) -> u_232 (aux2) -> bario
    #             -> krypton

    print(rs.find_inconsistency("Uranium-235", {"Auxiliary2"}))                 # Auxiliary1
    print(rs.find_inconsistency("Uranium-235", {"Auxiliary1", "Auxiliary2"}))   # None

    print("------------------------- R5 -------------------------")
    print(rs.simulate_reaction("Uranium-235", 20))   # ([('Krypton', 4.0), ('Bario', 3.0)], 258.4, 310.0)


if __name__ == "__main__":
    main()
