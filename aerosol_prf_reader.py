# Generates a plot of the resulting cloud structure from the aerosol.prf file. plots in density units reported in prf file
# Assumes 2 cloud profiles

import numpy as np
import matplotlib.pyplot as plt

# read ref file

reffile = './jupiter.ref'
with open(reffile,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    nlayers = int(all_data[2][2])
    ngas = int(all_data[2][3])
    alt_press_2=np.asfarray(all_data[3+1+ngas:])[:,:2]

# read aerosol file

aerosolprf = './output/aerosol.prf'

with open(aerosolprf,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    aerosol = np.asfarray(all_data[2:])

fig, axs = plt.subplots(figsize=(8,8),dpi=100)

plt.semilogy(aerosol[:,1],alt_press_2[:,1],label='Aerosol profile 1 (cloud)')
plt.semilogy(aerosol[:,2],alt_press_2[:,1],label='Aerosol profile 2 (haze)')

plt.gca().invert_yaxis()

plt.legend()
plt.ylabel('Pressure (atm)')
plt.xlabel('Density')
plt.show()