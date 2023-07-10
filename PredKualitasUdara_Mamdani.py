import numpy as np
import skfuzzy as fuzz
import pandas as pd
from skfuzzy import control as ctrl

def aqi(pm25_value, pm10_value):
    quality_evaluation = ctrl.ControlSystemSimulation(quality_ctrl)

    quality_evaluation.input['pm25'] = pm25_value
    quality_evaluation.input['pm10'] = pm10_value
    quality_evaluation.compute()

    quality_output = quality_evaluation.output['quality']

    if quality_output <= 3:
        kualitas_udara = 'Sehat'
    elif quality_output <= 6:
        kualitas_udara = 'Sedang'
    else:
        kualitas_udara = 'Tidak Sehat'

    print("Nilai AQI: {:.2f}".format(quality_output))
    print("Kualitas Udara: {}".format(kualitas_udara))

# Fuzzyfikasi variabel input dan output
pm25 = ctrl.Antecedent(np.arange(0, 301, 1), 'pm25')
pm10 = ctrl.Antecedent(np.arange(0, 301, 1), 'pm10')
quality = ctrl.Consequent(np.arange(0, 11, 1), 'quality')

#fungsi keanggotaan untuk variabel input
pm25['rendah'] = fuzz.trimf(pm25.universe, [0, 0, 50])
pm25['sedang'] = fuzz.trimf(pm25.universe, [51, 100, 150])
pm25['tinggi'] = fuzz.trimf(pm25.universe, [101, 300, 300])

pm10['rendah'] = fuzz.trimf(pm10.universe, [0, 0, 50])
pm10['sedang'] = fuzz.trimf(pm10.universe, [51, 100, 150])
pm10['tinggi'] = fuzz.trimf(pm10.universe, [101, 300, 300])

#fungsi keanggotaan untuk variabel output
quality['sehat'] = fuzz.trimf(quality.universe, [0, 3, 3])
quality['sedang'] = fuzz.trimf(quality.universe, [4, 5, 6])
quality['tidak_sehat'] = fuzz.trimf(quality.universe, [7, 10, 10])

#aturan fuzzy
aturan1 = ctrl.Rule(pm25['rendah'] & pm10['rendah'], quality['sehat'])
aturan2 = ctrl.Rule(pm25['sedang'] | pm10['sedang'], quality['sedang'])
aturan3 = ctrl.Rule(pm25['tinggi'] | pm10['tinggi'], quality['tidak_sehat'])

#sistem kontrol fuzzy
quality_ctrl = ctrl.ControlSystem([aturan1, aturan2, aturan3])

print("=====Kualitas Udara=====")
pm25_value = float(input("Masukkan nilai PM 2.5: "))
pm10_value = float(input("Masukkan nilai PM 10: "))
aqi(pm25_value, pm10_value)
