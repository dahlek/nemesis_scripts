import os
import numpy as np

'''
Runs Profile to regrid pressures
copies jupiter.prf file to jupiter.ref (.ref file has extra line at top)
Regrids aerosol.ref file

Be sure to run source_intel if running on Gattaca

'''

bar_per_atm = 1.01325
runname = 'jupiter'
num_aerosol_profiles = 1 # need to know for regridding aerosol.ref and fcloud.ref files
max_pressure = 10 # bars
min_pressure = 0.0001 # bars
num_layers = 55 # want 4-5 per scale height, or 5-8 km resolution in Jupiter's atmosphere
num_profiles = 1 # number of aerosol profiles

# convert to atm
max_pressure*=bar_per_atm
min_pressure*=bar_per_atm

# - - - - - - - - - -
# Run Profile to regrid runname.ref

file = open('./Profile_input','w') # input file that will regrid runname.ref 

file.write('y \n') # enter profile from existing file?
file.write(runname+' \n') # name of file
file.write('G \n') # Map profile onto new pressure grid
file.write(str(round(max_pressure,4))+' '+str(round(min_pressure,4))+' '+str(num_layers)+' \n')
file.write('H \n') # output profiles and exit
file.write(runname)
file.close()

os.system('Profile < Profile_input')


# pull info from new runname.prf file
with open('./'+runname+'.prf') as f:
    all_data=[x.split() for x in f.readlines()]
    n_press_layers = int(all_data[1][2])
    ngas = int(all_data[1][3])
    ref_array = np.asfarray(all_data[(3+ngas):])

# new altitude and pressure arrays
altitudes = ref_array[:,0]
pressures = ref_array[:,1]


# - - - - - - - - - -
# regrid aerosol.ref file
aerosol_string = ' '
for i in range(0,num_profiles):
    aerosol_string += ' 0.00000000 '

file = open('./aerosol_new.ref','w')
file.write('# aerosol.prf \n')
file.write('   '+str(num_layers)+'    '+str(num_profiles)+'  \n')
for i in range(0,num_layers):
    file.write(str(altitudes[i])+aerosol_string+' \n')
file.close()

#os.system('cp aerosol_new.ref aerosol_new.prf')

# - - - - - - - - - -
# regrid fcloud.ref file
fcloud_string = ' '
for i in range(0,num_profiles):
    fcloud_string += ' 1 '
fcloud_string += ' 1 '

file = open('./fcloud_new.ref','w')
file.write('   '+str(num_layers)+'    '+str(num_profiles)+'  \n')
for i in range(0,num_layers):
    file.write(str(altitudes[i])+fcloud_string+' \n')
file.close()

# ? Do I need to copy the fcloud.ref file to be the fcloud.prf file?


print('!!!Remember to copy jupiter.prf to be jupiter.ref and add extra line at header!!!')
print('!! make sure, if running continuous profile, that that input file is regridded too !!')
                                                                                                    85,1          Bot

