from math import pi, sqrt, e

def get_material_properties(mat_code):
    # Dictionary of materials with their properties
    material_properties = {
        "Al7068-T6": {
            "ult_ten_str": 710e6, #Pa,
            "yield": 683e6, #Pa,
            "young": 73.1e9, #Pa,
            "bearing_strength_allow": None, #cant find,
            "density": 2830, #kg/m3,
            "poisson": 0.32,
            "t_required": 1.32e-3 #m
        },
        "Ti6Al-4V(5)": {
            "ult_ten_str": 950e6, #Pa,
            "yield": 920e6, #Pa,
            "young": 113e9, #Pa,
            "bearing_strength_allow": None, #Pa,
            "density": 2780, #kg/m3
            "expansion_coef": None, # m/m * K,
            "poisson": 0.34,
            "t_required": 0.99e-3 #m         
        },
        "D6AC": {
            "ult_ten_str": 1931e6, #Pa,
            "yield": 1724e6, #Pa,
            "young": 210e9, #Pa,
            "bearing_strength_allow": None, #Pa,
            "density": 7.87e3, #kg/m3
            "expansion_coef": None, #m/m * K,
            "poisson": 0.3,
            "t_required": 0.49e-3 #m
        }    
    }
    # Returns the appropriate material properties based on the given material code
    return material_properties[mat_code]

def det_launch_loads(material, L, R, t_1, t_2, M_fuel, A_Z):
    # Get properties from material
    density = material["density"]
    yield_stress = material["yield"]
    E_modulus = material["young"]
    v = material["poisson"]
    t_1 = material["t_required"]
    # Set t to the thickness of the walls of the fuel tanks
    t = t_1 - 0.0001 
    # Margin of safety
    MS = 0.05
    safe = False
    counter = -1
    p = 17.04 * 100000 #Pa
    while not safe and counter <= 100000:
        # Increment counter and add 0.0001 m to thickness for analysis (iteration)
        counter += 1
        t += 0.0001
        # First calculate the initial mass of fuel tank mass plus fuel mass
        M_total = (2 * pi * R * t * density) + M_fuel 
        # Due to assumption, compressive load at the ends is the M_total time the max acceleration in z-direction
        F_z = M_total * A_Z
        #F_int_pressure_tension = (p - 101325) * pi * R**2  
        # Possible if we want to consider internal pressure that applies tension
        #F_z_total = F_z - F_int_pressure_tension
        F_z_total = 2
        if F_z_total < 0:
            print(F_z_total)
            safe = True
            print("There will be no compression so buckling is not possible.")
            break
        else:
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
            Q = (p / E_modulus) * (R / t)**2
                # Finnaly we find sigma_crit_shell_buckling
            sigma_crit_shell_buckling = (1.983 - 0.983 * e**(-23.14*Q)) * k * ((pi * E_modulus) / (12 * (1 - v **2))) * (t / L)**2
            
            #Comparing the stresses with material yield stress taking a 5% safety margin
            MS_column_buckling =  (yield_stress  / sigma_crit_column_buckling) - 1
            MS_shell_buckling = (yield_stress / sigma_crit_shell_buckling) - 1
            
            if MS_column_buckling > MS and MS_shell_buckling > MS:
                safe = True
    if safe:
        print("safe. t =", t)
    else:
        print("not safe.")
    
def attachment_mass(F_comp, N_attach): 
    # takes total compressive force as input, and returns mass of one attachment
    M_attach = (F_comp / N_attach) * (0.624) / 12100
    return M_attach