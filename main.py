import functions as fn
from math import pi

# initial dimensions
#   probably put them in a dict
# should include initial values, these aren't too hard to do by hand, and should be a reasonable starting point
# initial forces, come from initial masses, should be in function so they can be called in the loop again

# Basic masses (so payload, propellant and the likes, these values do not change)
M_const = 3850 - 1802  # kg, all not-structural masses, see wp2. (yeah 1800kg's of structure is a lot innit?)

# Basic dimensions (so length n shit)
l = 4.4  # meters
r = 0.5  # meters, minimum inner structure radius

# constants
g = 9.81  # standard gravity
# accelerations in all directions all in m/s/s
# Z is in negative Z direction, l is for lateral acceleration, so in XY plane.
#   script is written such that this is ok.
Al = 2 * g
Az = 4.6 * g

# Safety factors
Force_SF = 1.5  # SF applied to forces

MS_goal = 0.2  # well, speaks for itself innit

# add loop for material fuckery
# pull thickness from material :_)))
p = 20e5  # Pa, tank pressure

# some quick code to loop through materials
materials = ["Al7068-T6", "Ti6Al-4V(5)", "D6AC"]
for i in materials:
    matprob = fn.get_material_properties(i)
    ref_sigma_yield = matprob['yield']
    E_modulus = matprob["young"]
    v = matprob["poisson"]
    t = matprob["t_required"]
    num_iter = 0  # Counter which keeps count (no shit) on the number of iterations for the while loop
    Tank_pass = False
    Structure_pass = False
    finished = False
    while not finished and num_iter < 10000:
        num_iter += 1  # increment counter
        finished = True  # set finished to true, loop is broken if t is not changed
        Ixx = fn.SMoA_xx(r, t)  # second moment of area, called Ixx, but Iyy is the same because it's a circle :)))
        # update sc mass
        M = l * pi * ((r + t) ** 2 - r ** 2)
        M_total = M + M_const
        F_vect = fn.forces_on_top(M_total, Al, Az, Force_SF)  # returns array, [F_lateral, F_compressive]

        # calculate stresses
        # calc shear (just called tau because there's only one shear stress under consideration)
        tau_lateral = fn.calc_shear(t, Ixx, F_vect[0], r)  # shear due to lateral forces
        # no direction is considered, as the lateral force direction can always be defined as positive x, as it rotates

        # calc normal due to Az (fairly self explanatory)
        sigma_normal_axial = fn.calc_normal_axial(F_vect [1], r, t)
        # should be done

        # calc normal due to moment caused by shear force
        sigma_normal_shear = fn.calc_normal_shear(F_vect[0], l, r, Ixx)  # F_vect[0] is the lateral shear load

        # peak normal stress, to be compared against buckling and used for Von Mises failure
        sigma_normal_peak = sigma_normal_axial + sigma_normal_shear

        # hoop stress, used in Von Mises
        sigma_hoop = fn.hoop_stress(p, r, t)

        # Von Mises stress (used because it's simpler than Tresca, possible differences solved by safety factor)
        sigma_Von_Mises = fn.calc_von_mises(0, sigma_hoop, -sigma_normal_peak, tau_lateral, 0, 0)
        # sigma_Von_Mises_Struct = fn.calc_von_mises(0,0,sigma_normal_peak,tau_lateral,0,0)

        # calc reference stresses for buckling
        # shell
        ref_bkl_shell = fn.column_buckling_crit(E_modulus, Ixx, r, l, t)
        # column
        ref_bkl_column = fn.shell_buckling_crit(E_modulus, v, t, l, r, p)

        # calculate MS shear, normal, buckling (both, duh)
        MS_bkl_shell = fn.MS(ref_bkl_shell, sigma_normal_peak)
        MS_bkl_column = fn.MS(ref_bkl_column, sigma_normal_peak)
        MS_yield = fn.MS(ref_sigma_yield, sigma_Von_Mises)

        # makes changes and sets loop to run again
        if MS_goal < MS_bkl_shell < MS_goal * 1.1:
            finished = False
            if MS_goal > MS_bkl_shell:
                t *= 1.01
            else:
                t *= 0.99

        elif MS_goal < MS_bkl_column < MS_goal * 1.1:
            finished = False
            if MS_goal > MS_bkl_column:
                t *= 1.01
            else:
                t *= 0.99
        elif MS_goal < MS_yield < MS_goal * 1.1:
            finished = False
            if MS_goal > MS_yield:
                t *= 1.01
            else:
                t *= 0.99

        # if nothing changed, dimensions and relevant properties are printed
        if finished:
            print(i)
            print('Margins of safety:')
            print('Shell buckling: ', MS_bkl_shell)
            print('Column buckling: ', MS_bkl_column)
            print('Yield: ', MS_yield)
            print('Dimensions:')
            print('Thickness [m]: ', t)
            print('Structure mass [kg]: ', M)