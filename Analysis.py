import numpy as np
import pandas as pd
# from matplotlib import pyplot as plt
import Reactor_V1 as rf

data = pd.read_csv('Run_5P_edit.csv')
hplc_data = pd.read_excel('Data.xlsx', sheet_name = 'Run 5P')

# time = np.array(data['Time'])
# r_co2 = np.array(data['CO2_rate_(mol/Cmol/min)'])
# r_o2 = np.array(data['O2_rate_(mol/Cmol/min)'])
# dosing_avg = np.nan_to_num(np.array(data['Dosing_average_(on/off)']))
# dosing_rpm = np.array(data['Dosing_(RPM)'])
# dosing_raw = np.array(data['Dosing'])
# comp_co2 = np.array(data['Gas_analyser_CO2%'])
# comp_o2 = np.array(data['Gas_analyser_O2%'])
# flow_co2 = np.array(data['CO2_Flow_rate(ml/min)'])
# flow_o2 = np.array(data['O2_Flow_rate_(ml/min)'])
# temp = np.array(data['Temperature(C)'])
# 
# i_start = int(len(time) * 110.5/time[-1])
# 
# sum_avg = np.sum(dosing_avg[i_start::])
# sum_raw = np.sum(dosing_raw[i_start::])
# 
# error = (sum_avg - sum_raw)/sum_raw *100
# 
# rpm = 2
# mmx = 24.04 # g/cmol C H 1.8 O 0.5 N 0.16
# 
# flowrate_naoh = dosing_avg * (0.05228291711 * rpm - 0.005367597828)/1000 #l/min
# rate_f = 10 * 0.5 * flowrate_naoh * (1.087/(1.93/mmx)) # mol/l * mol_f/mol_naoh * ml/min = mmol/min
# 
# plt.plot(time[i_start::],rate_f[i_start::], 'k')
# plt.plot(time[i_start::],data['Fumaric_rate_(Cmol/Cmol/min)'][i_start::]*1000)
# plt.show()
# 
# comp_co2_0 = 8.4768/100 #%
# comp_o2_0 = 19.894/100 #%
# 
# 
# Qtotal = (flow_co2 + flow_o2)/1000 #L/min
# Ftotal = Qtotal*P/(R*temp)
# Fco2_in = Qtotal*P/(R*temp)*comp_co2_0
# Fo2_in = Qtotal*P/(R*temp)*comp_o2_0
# Fco2_out = Qtotal*P/(R*temp)*comp_co2
# Fo2_out = Qtotal*P/(R*temp)*comp_o2
# 
# mx = 1.93 / 24.04 #mol_x
# 
# r_co2_cal = (Fco2_out - Fco2_in)/mx
# r_o2_cal = (Fo2_out - Fo2_in)/mx