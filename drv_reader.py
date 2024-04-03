# generates a plot of optical depth/atm as a function of pressure. * should convert to bars

import matplotlib.pyplot as plt
import numpy as np

drvfile = './output/jupiter.drv'

pressure_drv = []
bottom_pressure_drv = []
optdepth_cloud1 = []
optdepth_cloud2 = []

with open(drvfile,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    pressurepoints = int(all_data[6][0])
    data = all_data[25:259]
    for i in range(0,pressurepoints):
        pressure_drv.append(float(data[(6*i)][6])) # pressure at center of layer
        bottom_pressure_drv.append(float(data[(6*i)][3])) # pressure at bottom of layer
        optdepth_cloud1.append( float(data[4+(6*i)][0]) )
        optdepth_cloud2.append( float(data[4+(6*i)][1]) )

optdepth_cloud1_perbar = []
optdepth_cloud2_perbar = []

# calculate optical depth per bar (divide each optical depth amount by the width of that pressure bin)
for i in range(0,pressurepoints-1):
    pressure_width = bottom_pressure_drv[i]-bottom_pressure_drv[i+1]
    optdepth_cloud1_perbar.append(optdepth_cloud1[i]/pressure_width)
    optdepth_cloud2_perbar.append(optdepth_cloud2[i]/pressure_width)

fig, axs = plt.subplots(figsize=(8,8))

plt.semilogy(optdepth_cloud1_perbar,pressure_drv[:-1],label='Main cloud; total optical depth: '+str(round(sum(optdepth_cloud1),3)))
plt.semilogy(optdepth_cloud2_perbar,pressure_drv[:-1],label='Chromohpore haze; total optical depth: '+str(round(sum(optdepth_cloud2),3)))

plt.gca().invert_yaxis()
plt.ylabel('Pressure (bars)')
plt.xlabel('Optical depth/atm')
plt.title('Aerosol profiles')
plt.tight_layout()
plt.subplots_adjust(hspace=0.0)
plt.legend()
plt.show()