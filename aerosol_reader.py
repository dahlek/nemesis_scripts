import numpy as np
import matplotlib.pyplot as plt

'''
Reads aerosl.prf file, plots out aersol profiles
'''

directory = './'
aerosol_file = 'aerosol.prf'
ref_file = 'jupiter.ref' # use to pull pressure values

aerosol = directory+aerosol_file
ref = directory+ref_file

# pull pressure values for each layer
with open(ref,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    ngas = int(all_data[2][3]) # number of gases (lines) to skip
    nlayers = int(all_data[2][2]) # number of layers
    press = np.asfarray(all_data[(4+ngas):(4+ngas+nlayers)])[:,1]

with open(aerosol,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    nlayers=int(all_data[1][0]) # number of layers
    nclouds=int(all_data[1][1]) # number of clouds
    for j in range(1,nclouds+1):
        aero_profile = np.asfarray(all_data[2:])[:,j]
        plt.semilogy(aero_profile,press)


print 'number of aerosol profiles:',nclouds

# Plot:
#plt.ylim(10,0.01)
plt.gca().invert_yaxis()
plt.ylabel('Pressure (atm)')
plt.xlabel('Specfiic density (particles/gram)')
plt.title('Aerosol profile')
plt.show()
