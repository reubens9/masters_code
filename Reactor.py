
# coding: utf-8

import numpy as np

def math_test(a,b,c):
    # a = X[0]
    # b = X[1]
    # c = X[2]
    return a*b*c

MMx = 24.04 # g/cmol C H 1.8 O 0.5 N 0.16
Q = 0.9058  # mL/min
C_N = 0.0125  # g/L
r_Urea = Q / 1000 * C_N  # g Urea/min
Mass_fr_Urea = 14 * 2 / (12 + 4 + 28 + 16)
Mass_fr_Biomass = 14 * 0.16 / (12 + 1.8 + 8 + 0.16 * 14)
M_x = 1.9343 # g
r_Biomass = r_Urea * Mass_fr_Urea / Mass_fr_Biomass / M_x  # CmolX/CmolX/min

def rates(r_CO2, r_O2, r_FA):
    A = 0.1
    PO = 1.5
    G = 1.8
    B = 0.1
    T = 0.1
    # Q = 0.9058 # mL/min
    # C_N = 0.0125 # g/L
    # r_Urea = Q/1000*C_N # g Urea/min
    # Mass_fr_Urea = 14*2/(12+4+28+16)
    # Mass_fr_Biomass = 14*0.16/(12 + 1.8 + 8 + 0.16*14)
    # r_Biomass = r_Urea * Mass_fr_Urea / Mass_fr_Biomass

    A = np.matrix([#v0      v1     v2      v3      v4      v5      v6      v7      v8
                  [-1,  (1+A),      1,      1,      0,      0,      0,      0,      0],     #node
                   [0,      0,      0,     -1,      1,      1,      0,      0,      0],     #node
                   [0,      0,      0,      0,      0,     -1,    2/3,    3/4,      0],     #node
                   [0,     -G,    2/3,      0,      0,    1/3,      0,   -1/4,   2*PO],     #ATP
                   [0,      B,      2,      0,   -1/3,    1/3,   -1/2,   -1/4,     -2],     #NADH
                   [0,      A,      1,      0,      0,      0,    1/3,   -1/4,      0],     #CO2
                   [0,      0,      0,      0,      0,      0,      0,      0,      1],     #O2
                   [0,      0,      0,      0,      0,      0,      0,      1,      0],     #Fumaric
                   [0,      1,      0,      0,      0,      0,      0,      0,      0]])

    B = np.matrix( [0,      0,      0,      T,      0,  r_CO2,   r_O2,   r_FA,      r_Biomass] )

    rate = np.linalg.solve(A, B)

    return (rate[6, 0])   #Ethanol


def gas_rate_O2(Cin, Cout, Qin, m):
    """ Qin: mL/min P: atm """

    P = 1 # atm
    R = 0.08205746 # L atm/mol K
    T = 35 + 273.15 # K
    M_x = m/MMx # Cmol
    Vrxn = 2.603 # L gas phase reactor volume
    Q = Qin/1000

    F_total = P*Q/R*T
    Fin = F_total*Cin/100
    Fout = F_total*Cout/100
    rO2v = 1/Vrxn*(Fin - Fout)
    rO2x = rO2v*Vrxn/M_x
    return (rO2x) # mol/CmolX/min

def fumaric_rate(dosing_avg, RPM, m):
    M_x = m/ MMx
    Q = 0.042*RPM/1000  * dosing_avg # L/min/Vrxn
    C_NaOH = 10 #mol/L
    F_NaOH = Q*C_NaOH  # mol/min/Vrxn
    F_FA = F_NaOH/2  * 1.087/M_x  # mol/min/CmolX
    return (F_FA)
