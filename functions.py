from math import pi, sqrt

def get_material_properties(mat_code):
    # Dictionary of materials with their properties
    material_properties = {
        #...
    }
    # Returns the appropriate material properties based on the given material code
    return material_properties[mat_code]

def det_launch_loads(material, L, R, t_1, t_2, M_fuel, A_Z):
    # Get properties from material
    density = material["density"]
    yield_stress = material["yield"]
    E_modulus = material["young"]
    v = material["poisson"]
    # Set t to the thickness of the walls of the fuel tanks
    t = t_1
    # First calculate the initial mass of fuel tank mass plus fuel mass
    M_total = 2 * pi * R * t * density + M_fuel
    # Due to assumption, compressive load at the ends is the M_total time the max acceleration in z-direction
    F_z = M_total * A_Z
    # Determination of cross section area
    A = 2 * pi * (R + t)**2
    # Determination of cross section Moment of Inertia
    Ixx = (pi/4) * ((R + t)**4 - R**4)
    # Determination of the critical stress for Column Buckling
    sigma_crit_column_buckling = (pi * E_modulus * Ixx) / (A * L **2)
    # Shell Buckling determination
        # First use the derivative (check report) to find lambda
    lambda_ = sqrt((12 / pi**4) * (L**4 / (R**2 * t**2)) * (1 - v**2))
        # Secondly we find the value of k
    k = lambda_ + (12 / pi**4) * (L**4/(R**2 * t**2)) * (1 - v**2) * (1 / (lambda_**2))
        # Thirdly we find the value of Q
    Q = (p / E) * (R / t)**2
        # Finnaly we find sigma_crit_shell_buckling
    sigma_crit_shell_buckling = (1.983 - 0.983 * e^(-23.14*Q)) * k * ((pi * E) / (12 * (1 - v **2))) * (t / L)**2

    pass