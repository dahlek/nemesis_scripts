import numpy as np
#from scipy.interpolate import pchip
import matplotlib.pyplot as plt

# Pull info out of mre file
plot_fit_and_data = 1 # turn on plot for fit and data 

#directory = '/home/praesepe/dahlek/testNEB_test/'
#directory = '/home/users/dahlek/agu_nemesis_2/testNEB_sub_cont_nh3_export/'
#directory = '/home/praesepe/dahlek/pj5_1_ez/'
#directory = '/home/praesepe/dahlek/pats_files_my_spectra/'
#directory = '/home/praesepe/dahlek/paper_models/pj5_4/'
#directory = '/home/praesepe/dahlek/paper_models/pj5_seb/'
directory = './'
mrefile = directory+'jupiter.mre'
logfile = directory+'jupiter.log'
spx = directory+'jupiter.spx'

with open(mrefile,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    #print all_data[0] # print the first line. will be a list.
    nlines=int(all_data[1][2]) # length of spectrum
    spec=np.asfarray(all_data[5:5+nlines]) # Pull all the spectral data, the bulk of the mre file !!!Hard coded distance from the top of the file
    wl = spec[:,1]  # wavelength in microns
    R_meas = spec[:,2] # Measured radiance (data)
    error = spec[:,3] # error
    R_fit = spec[:,5] # Fit radiance


# open log file and find chisq/ny
with open(logfile,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    for i in range(len(all_data)-200,len(all_data)):
        if len(all_data[i]) == 0:
            continue
        if all_data[i][0] == 'chisq/ny':
            chisq = all_data[i][2]
            break

# plot data and fit
plt.fill_between(wl,R_meas+error,R_meas-error,color='gray')
plt.plot(wl,R_meas,'black')
plt.plot(wl,R_fit)
plt.title('chisq/ny = '+str(chisq))
plt.xlim(.470,.951)
plt.ylabel('Radiance, nW/cm2/ster/micron')
plt.xlabel('Wavelength (microns)')
plt.legend(['Measured radiance','Fit radiance'])
plt.show()
