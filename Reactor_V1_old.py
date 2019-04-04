
# coding: utf-8

def say_my_name(name1):
    return 'Hello ' + name1

def math_test(a,b,c):
    # a = X[0]
    # b = X[1]
    # c = X[2]
    return a*b*c

MMx = 24.04 # g/cmol C H 1.8 O 0.5 N 0.16
MMfa = 12+1+16 #g/cmol
MMsa = 12+1.5+16 #g/cmol
MMgly = 12 + 8/3 + 16 # g/cmol
Q = 0.9058  # mL/min
C_N = 0.0125  # g/L
r_Urea = Q / 1000 * C_N  # g Urea/min
Mass_fr_Urea = 14 * 2 / (12 + 4 + 28 + 16)
Mass_fr_Biomass = 14 * 0.16 / (12 + 1.8 + 8 + 0.16 * 14)
M_x = 1.9343 # g
r_Biomass = r_Urea * Mass_fr_Urea / Mass_fr_Biomass / M_x  # CmolX/CmolX/min

import time




from numpy import matrix, linalg



def ethanol_rate(r_CO2, r_O2, r_FA, m):

    y_fagy = 0.11  # g/g
    y_fasa = 0.04  # g/g
    Y_fagy = y_fagy * MMfa / MMgly
    Y_fasa = y_fasa * MMfa / MMsa

    A = matrix([  # Glucose  O2        Urea      Biomass   CO2       H2O       Fumaric   Succinic  Ethanol   Glycerol
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1],  # C
        [2, 0, 4, 1.8, 0, 2, 1, 1.5, 3, 8 / 3],  # H
        [1, 2, 1, 0.5, 2, 1, 1, 1, 0.5, 1],  # O
        [0, 0, 2, 0.16, 0, 0, 0, 0, 0, 0],  # N
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # O2
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # CO2
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # FA
        [0, 0, 0, 0, 0, 0, Y_fagy, 0, 0, -1],  # Yfagy
        [0, 0, 0, 0, 0, 0, Y_fasa, -1, 0, 0],  # Yfasa
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], ])  # mu

    r_Biomass = r_Urea * Mass_fr_Urea / Mass_fr_Biomass / m  # CmolX/CmolX/min

    B = matrix([0,        0,        0,        0,      r_O2,   r_CO2,     r_FA,        0,        0,        r_Biomass] ).T

    rate = linalg.solve(A, B)

    return (rate[8, 0])   #Ethanol

def gas_rate(Cin, Cout, Qin, m):
    """ Qin: mL/min P: atm """

    P = 1 # atm
    R = 0.08205746 # L atm/mol K
    T = 35 + 273.15 # K
    M_x = m/MMx # Cmol
    Vrxn = 0.563 # L gas phase reactor volume
    Q = Qin/1000

    F_total = P*Q/R*T
    Fin = F_total*Cin/100
    Fout = F_total*Cout/100
    r_v = 1/Vrxn*(Fout - Fin)
    r_x = r_v*Vrxn/M_x
    return (r_x) # mol/CmolX/min

def fumaric_rate(dosing_avg, RPM, m):
    M_x = m/ MMx
    y_fasa = 0.04  # g/g
    Y_fasa = y_fasa * MMfa / MMsa
    Q = 0.042*5/1000  * dosing_avg # L/min/Vrxn
    C_NaOH = 10 # mol/L
    F_NaOH = Q*C_NaOH  # mol/min/Vrxn
    F_FA = F_NaOH/2  * 1.087/M_x * (1/(Y_fasa + 1))  # mol/min/CmolX  Also accounting for the production of succinic
    return (F_FA)


start = time.time()

CinO = 18.5
CinC = 10
CoutO = 17.5
CoutC = 11
M = 1.9
Qin = 108
dosing = 0.5

r_o  = gas_rate(CinO, CoutO, Qin, M)
r_co = gas_rate(CinC, CoutC, Qin, M)
r_fa = fumaric_rate(dosing,5,M)
r_e = ethanol_rate(r_co, r_o, r_fa, M)

print (r_o, r_co, r_fa, r_e)

end = time.time()

print (end - start)
