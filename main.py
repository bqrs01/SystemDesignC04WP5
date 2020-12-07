from functions import det_launch_loads, get_material_properties

L = 1.63
R = 1 / 2 #m
g = 9.81 #m/s2
Az = 4.56 * g #m/s2
M_fuel = 1127.9 #kg
possible_materials = ["Al7068-T6", "Ti6Al-4V(5)", "D6AC"]

for mat_code in possible_materials:
    print("Trying", mat_code)
    material = get_material_properties(mat_code)
    det_launch_loads(material, L, R, None, None, M_fuel, Az)
    print()