from math import e, pi, sqrt
import numpy as np


def get_material_properties(mat_code):
    # Dictionary of materials with their properties
    material_properties = {
        "Al7068-T6": {
            "ult_ten_str": 710e6,  # Pa,
            "yield": 683e6,  # Pa,
            "young": 73.1e9,  # Pa,
            "bearing_strength_allow": None,  # cant find,
            "density": 2830,  # kg/m3,
            "poisson": 0.32,
            "t_required": 1.94e-3  # m
        },
        "Ti6Al-4V(5)": {
            "ult_ten_str": 950e6,  # Pa,
            "yield": 920e6,  # Pa,
            "young": 113e9,  # Pa,
            "bearing_strength_allow": None,  # Pa, N/a
            "density": 2780,  # kg/m3
            "expansion_coef": None,  # m/m * K,
            "poisson": 0.34,
            "t_required": 1.45e-3  # m
        },
        "D6AC": {
            "ult_ten_str": 1931e6,  # Pa,
            "yield": 1724e6,  # Pa,
            "young": 210e9,  # Pa,
            "bearing_strength_allow": None,  # Pa, N/a
            "density": 7.87e3,  # kg/m3
            "expansion_coef": None,  # m/m * K,
            "poisson": 0.3,
            "t_required": 0.71e-3  # m
        }
    }
    # Returns the appropriate material properties based on the given material code
    return material_properties[mat_code]


def attachment_mass(F_comp, N_attach):  # takes total compressive force as input, and returns mass of one attachment
    m_attach = (F_comp / N_attach) * (0.6) / 12100
    return m_attach


def SMoA_xx(R, t):  # calculates Ixx for a circle, so it's also Iyy
    Ixx = 0.25 * pi * ((R + t) ** 4 - R ** 4)
    return Ixx


def column_buckling_crit(E_modulus, Ixx, r, L, t):  # calculates column buckling
    A = pi * ((t + r) ** 2 - r ** 2)  # area of material
    sigma_cr_column = (pi * E_modulus * Ixx) / (A * L ** 2)
    return sigma_cr_column


def shell_buckling_crit(E_modulus, v, t, L, R, p):
    # Q, Lambda, k all req'd for shell buckling critical stress
    Q = (p / E_modulus) * (R / t) ** 2  # find Q
    lambda_ = sqrt((12 / pi ** 4) * (L ** 4 / (R ** 2 * t ** 2)) * (1 - v ** 2))  # find lambda
    k = lambda_ + (12 / pi ** 4) * (L ** 4 / (R ** 2 * t ** 2)) * (1 - v ** 2) * (1 / (lambda_ ** 2))  # find k
    sigma_cr_shell = (1.983 - 0.983 * e ** (-23.14 * Q)) * k * ((pi * E_modulus) / (12 * (1 - v ** 2))) * (t / L) ** 2
    return sigma_cr_shell


def forces_on_top(m_struct, al, az,
                  force_SF):  # returns forces acting on the beam. SC simplified to point at centre structure
    a_vect = np.array([al, az])
    f_vect = a_vect * m_struct * force_SF
    return f_vect


def MS(sigma_Ref, sigma_Appl):
    ms = (sigma_Ref / sigma_Appl) - 1
    return ms


######################################
# working space )))))
def calc_shear(t, Ixx, Vy, r):
    tau = Vy * t * r / Ixx
    return tau


def calc_normal_axial(F_z, r, t):
    A = pi * ((t + r) ** 2 - r ** 2)
    sigma_axial = F_z / A
    return sigma_axial


def calc_normal_shear(F_lateral, length, radius, Ixx):  # Returns normal stress due to lateral shear load
    # Find magnitude of moment due to shear
    moment_magnitude = F_lateral * length

    # Uses the bending formula (M*y/Ixx) to find normal stress due to the shear load
    normal_due_to_shear = (moment_magnitude * radius) / Ixx

    return normal_due_to_shear


def calc_von_mises(sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx):
    # full Von Mises equation
    sigma = sqrt(0.5 * (sigma_x - sigma_y) ** 2 + (sigma_y - sigma_z) ** 2 + (sigma_z - sigma_x) ** 2 + 3 * (
                tau_xy ** 2 + tau_yz ** 2 + tau_zx ** 2))
    # sigma = sqrt((sigma ** 2) + (3 * (tau ** 2)))  # simplified, only considering one normal, and one shear stress
    return sigma


def hoop_stress(p, r, t): # hoop stress in pressure vessele
    sigma_hoop = p * r / t
    return sigma_hoop


def axial_stress(p, r, t): # axial stress in pressure vessel
    sigma_axial = p*r/(2*t)
    return sigma_axial