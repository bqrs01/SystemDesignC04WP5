import numpy as np
r = 0.5 #m
h = 2*r - np.sqrt((2*r)**2-r**2)#m
print("h = {} m".format(round(h,2)))
def vol_cap(r, h):
    V_cap = (np.pi*(-np.sqrt(3)+2)*((2*r)**3)/(3))-((1/3)*(2*r-h)*(np.pi*r**2))
    return V_cap

V_fuel = 657 #L
V_oxi = 416 #L

print("V_fuel = {} L and V_oxi = {} L".format(V_fuel,V_oxi))

cap = vol_cap(r, h)
cap = cap*(1000/1) #L
print("Volume of one cap: {} L".format(round(cap,2)))
cap *= 2

V_fuel -= cap #L
V_oxi -= cap #L

# print(round(V_fuel,2),round(V_oxi,2))

print("Volume of two cap: {} L".format(round(cap,2)))

V_fuel = V_fuel*(1/1000) #m^3
V_oxi = V_oxi*(1/1000) #m^3

def l_c(r, V):
    l_cc = V/(np.pi*r**2)
    return l_cc

l_c_oxi = l_c(r,V_oxi)
l_c_fuel = l_c(r,V_fuel)

t = 1.5 #mm
rho = 2830 #km/m^3

def surface(r,h,l_c):
    S = 4*np.pi*(2*r)*h+2*np.pi*r*l_c
    return S

S_fuel = surface(r, h, l_c_fuel)
S_oxi = surface(r, h, l_c_oxi)

# print(round(S_fuel,2),round(S_oxi,2))

m_fuel = t*1e-3*S_fuel*rho #kg
m_oxi = t*1e-3*S_oxi*rho #kg

print("m_fuel = {} kg and m_oxi = {} kg".format(round(m_fuel,3), round(m_oxi,3)))

l_c_oxi *= 100 #cm
l_c_fuel *= 100 #cm

print("l_c_oxi = {} cm and l_c_f = {} cm".format(round(l_c_oxi,2),round(l_c_fuel,2)))

h *= 100 #cm
def len_tank(l_c,h):
    len = l_c + 2*h
    return len

l_fuel = len_tank(l_c_fuel, h)
l_oxi = len_tank(l_c_oxi, h)

print("l_oxi = {} cm and l_fuel = {} cm".format(round(l_oxi,2),round(l_fuel, 2)))

l_total = l_fuel+l_oxi
print("total length: {} m".format(round(l_total/100,2)))