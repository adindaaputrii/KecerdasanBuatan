import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#fuzzyfikasi variabel input dan output
pm25 = ctrl.Antecedent(np.arange(0, 201, 1), 'pm25')
pm10 = ctrl.Antecedent(np.arange(0, 201, 1), 'pm10')
quality = ctrl.Consequent(np.arange(0, 11, 1), 'quality')

#fungsi keanggotaan variabel input
pm25['rendah'] = fuzz.trimf(pm25.universe, [0, 0, 50])
pm25['sedang'] = fuzz.trimf(pm25.universe, [40, 75, 100])
pm25['tinggi'] = fuzz.trimf(pm25.universe, [100, 200, 200])

pm10['rendah'] = fuzz.trimf(pm10.universe, [0, 0, 50])
pm10['sedang'] = fuzz.trimf(pm10.universe, [40, 75, 100])
pm10['tinggi'] = fuzz.trimf(pm10.universe, [100, 200, 200])

#fungsi keanggotaan variabel output
quality['sehat'] = fuzz.trimf(quality.universe, [0, 3, 3])
quality['sedang'] = fuzz.trimf(quality.universe, [4, 6, 6])
quality['tidak_sehat'] = fuzz.trimf(quality.universe, [7, 10, 10])

#aturan fuzzy
aturan1 = ctrl.Rule(pm25['rendah'] & pm10['rendah'], quality['sehat'])
aturan2 = ctrl.Rule(pm25['sedang'] | pm10['sedang'], quality['sedang'])
aturan3 = ctrl.Rule(pm25['tinggi'] | pm10['tinggi'], quality['tidak_sehat'])

#sistem kontrol fuzzy
quality_ctrl = ctrl.ControlSystem([aturan1, aturan2, aturan3])

#inisialisasi simulasi kontrol sistem
quality_evaluation = ctrl.ControlSystemSimulation(quality_ctrl)

def aqi(pm25_value, pm10_value, expected_output):
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

    # Hitung nilai error
    error = abs(expected_output - quality_output)
    return error

#data
data = [
    {"pm25": 126, "pm10": 73, "aqi": 6.5},
    {"pm25": 70, "pm10": 53, "aqi": 6.0},
    {"pm25": 53, "pm10": 32, "aqi": 6.0},
    {"pm25": 59, "pm10": 36, "aqi": 6.0},
    {"pm25": 51, "pm10": 29, "aqi": 6.0},
    {"pm25": 45, "pm10": 24, "aqi": 2.05},
    {"pm25": 55, "pm10": 33, "aqi": 6.0},
    {"pm25": 57, "pm10": 38, "aqi": 6.0},
    {"pm25": 45, "pm10": 29, "aqi": 2.05},
    {"pm25": 45, "pm10": 32, "aqi": 2.05},
    {"pm25": 118, "pm10": 81, "aqi": 6.29},
    {"pm25": 109, "pm10": 73, "aqi": 6.13},
    {"pm25": 113, "pm10": 74, "aqi": 6.20},
    {"pm25": 105, "pm10": 73, "aqi": 6.07},
    {"pm25": 102, "pm10": 69, "aqi": 6.02},
    {"pm25": 119, "pm10": 78, "aqi": 6.31},
    {"pm25": 104, "pm10": 63, "aqi": 6.05},
    {"pm25": 33, "pm10": 19, "aqi": 2.16},
    {"pm25": 90, "pm10": 64, "aqi": 6.0},
    {"pm25": 70, "pm10": 56, "aqi": 6.0},
    {"pm25": 93, "pm10": 62, "aqi": 6.0},
    {"pm25": 18, "pm10": 21, "aqi": 2.25},
    {"pm25": 57, "pm10": 142, "aqi": 7.38},
    {"pm25": 91, "pm10": 60, "aqi": 6.0},
    {"pm25": 72, "pm10": 53, "aqi": 6.0},
    {"pm25": 93, "pm10": 62, "aqi": 6.0},
    {"pm25": 100, "pm10": 68, "aqi": 6.0},
    {"pm25": 93, "pm10": 68, "aqi": 6.0},
    {"pm25": 100, "pm10": 66, "aqi": 6.0},
    {"pm25": 93, "pm10": 64, "aqi": 6.0},
    {"pm25": 95, "pm10": 53, "aqi": 6.0},
    {"pm25": 86, "pm10": 61, "aqi": 6.0},
    {"pm25": 99, "pm10": 65, "aqi": 6.0},
    {"pm25": 93, "pm10": 67, "aqi": 6.0},
    {"pm25": 80, "pm10": 55, "aqi": 6.0},
    {"pm25": 58, "pm10": 179, "aqi": 7.78},
    {"pm25": 124, "pm10": 69, "aqi": 6.42},
    {"pm25": 136, "pm10": 78, "aqi": 6.57},
    {"pm25": 102, "pm10": 65, "aqi": 6.02},
    {"pm25": 121, "pm10": 75, "aqi": 6.35},
]

total_error = 0
jumlah_benar = 0 

#hitung dan tampilkan hasil aqi
for i in range(len(data)):
    print("--","Data ke-", i+1, "---")
    print("PM2.5:", data[i]["pm25"])
    print("PM10:", data[i]["pm10"])
    error = aqi(data[i]["pm25"], data[i]["pm10"], data[i]["aqi"])
    total_error += error
    print("Error: {:.2f}".format(error))
    print()

    if quality_evaluation.output['quality'] <= 3 and data[i]["aqi"] <= 3:
        jumlah_benar += 1
    elif (
        quality_evaluation.output['quality'] > 3 and
        quality_evaluation.output['quality'] <= 6 and
        data[i]["aqi"] > 3 and
        data[i]["aqi"] <= 6
    ):
        jumlah_benar += 1
    elif quality_evaluation.output['quality'] > 6 and data[i]["aqi"] > 6:
        jumlah_benar += 1

average_error = total_error / len(data)
akurasi = (jumlah_benar / len(data)) * 100

print("Rata-rata Error: {:.2f}".format(average_error))
print("Akurasi: {:.2f}%".format(akurasi))
