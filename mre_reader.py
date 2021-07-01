import numpy as np
import matplotlib.pyplot as plt

directory = './'
runname = 'jupiter'

mrefile = directory+runname+'.mre'
logfile = directory+'runname'+'.log'
spx = directory+runname+'.spx'

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
plt.ylabel('Radiance, nW/cm2/ster/micron')
plt.xlabel('Wavelength (microns)')
plt.legend(['Measured radiance','Fit radiance'])
plt.show()
