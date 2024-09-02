import numpy as np

'''
Makes a new fcloud.ref file; useful after using Profile to reconfigure atmospheric pressure levels, since Nemesis will make new .ref files but not new fcloud.ref files.
This version assumes 3 clouds; change the number of 1's in the second for loop to adjust cloud numbers
'''

#pressure_levels = 108 # how many levels
pressure_levels = 39

ref_file = './jupiter.ref'

# read heights from .ref file
height = []

with open(ref_file,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    for i in range(11,len(all_data)):
        height.append(float(all_data[i][1])) # pressure


# make new fcloud file
#file = open('/Users/dahlek/Desktop/parameterization_tests/CB_cloud_new_pressures/fcloud_new.ref','w')
file = open('./aerosol_apr.dat','w')
file.write('   '+str(pressure_levels)+'    1.5  \n') # correlation length
for i in range(0,pressure_levels):
    file.write(str(height[i])+'  0.001  0.0002 '+' \n') # aerosol density and variance; allowing 20%
file.close()
