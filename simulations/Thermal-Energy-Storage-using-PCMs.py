#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
try:
    base_dir = Path().resolve().parent
except:
    base_dir = Path(__file__).parent.parent.resolve()
plots_dir = base_dir / 'plots'
simulations_dir = base_dir / 'simulations'
csvs_dir = base_dir / 'csvs'
os.makedirs(plots_dir, exist_ok = True)
os.makedirs(simulations_dir, exist_ok = True)
os.makedirs(csvs_dir, exist_ok = True)

# Properties of PCMs

pcms = {'Paraffin Wax': {'Tm': 55.0, 'L': 200000.0, 'cp_solid': 2000.0, 'cp_liquid': 2300.0}, 
        "Stearic Acid": {"Tm": 69.0, "L": 170000.0, "cp_solid": 2200.0, "cp_liquid": 2300.0}, 
        "Salt Hydrate": {"Tm": 32.0, "L": 250000.0, "cp_solid": 1500.0, "cp_liquid": 1800.0}}
m = 1.0
P = 200.0
dt = 1.0
total = 2000.0
T0 = 25.0
results = {}

# Running simulation for each PCM

for name, data in pcms.items():
    Tm = data['Tm']
    L = data['L']
    cp_solid = data['cp_solid']
    cp_liquid = data['cp_liquid']
    T = T0
    Q_melt = m*cp_solid*(Tm - T0) + m*L
    Q_total = 0
    time = []
    temperature = []
    energy = []

    # Simulation and saving results

    for t in np.arange(0, total, dt):
        Q_total = Q_total + P*dt
        if T < Tm:
            T = T + (P*dt)/(m*cp_solid)
        elif T >= Tm and Q_total < Q_melt:
            T = Tm
        else:
            T = T + (P*dt)/(m*cp_liquid)
        time.append(t)
        temperature.append(T)
        energy.append(Q_total/1000) # (/1000) To convert energy into kilo joules
    results[name] = {'time': time, 'temperature': temperature, 'energy': energy, 'Q_total': (Q_total/1000)}

# Temperature versus Time Plot

plt.figure(figsize = (8,4))
for name, data in results.items():
    plt.plot(data['time'], data['temperature'], label = name)
plt.title("Temperature vs Time (All PCMs)")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.savefig(plots_dir / 'temperature_vs_time.png', dpi = 300)
plt.show()

# Energy versus Time Plot

plt.figure(figsize = (8,4))
for name, data in results.items():
    plt.plot(data['time'], data['energy'], label = name)
plt.title('Energy vs Time (All PCMs)')
plt.xlabel('Time (s)')
plt.ylabel('Energy (kJ)')
plt.legend()
plt.savefig(plots_dir / 'energy_vs_time.png', dpi = 300)
plt.show()

# Saving results to CSV

for name, data in results.items():
    df = pd.DataFrame({'time_s': data['time'],
        'temperature_C': data['temperature'],
        'energy_kJ': data['energy']})
    file_name = f"{name.replace(' ', '_')}_simulation.csv"
    df.to_csv(csvs_dir / file_name, index=False)
    print(f"Saved CSV: {file_name}")

# Print summary of total energy stored

print('The energy stored by each PCM is:')
for name, data in results.items():
    print(f'{name}: {data['Q_total']}kJ')


# In[ ]:




