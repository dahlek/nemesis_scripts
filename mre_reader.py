import numpy as np
import matplotlib.pyplot as plt

'''
Reads .mre file, plots measured and fit spectra. Accounts for different numbers of spectra/datapoints and calculates reduced chi squared from the .mre file
Emma Dahl, 2021
'''

directory = './'
runname = 'jupiter'
mrefile = directory+runname+'.mre'

def reduced_chi_sq_finder(data,data_error,model):
    '''
    Takes two arays of the same dimension, calculates the chi sqaured value
    Adapted from chi2.pro from James Sinclair
    '''
    N = len(data)
    tmp = (data-model)/data_error
    chi_sq = np.sum(tmp**2)/N
    return chi_sq

with open(mrefile,'r') as f:
    all_data=[x.split() for x in f.readlines()]
    #print all_data[0] # print the first line. will be a list.
    nlines=int(all_data[1][2]) # length of spectrum
    n_spec = int(all_data[1][1])
    spec=np.asfarray(all_data[5:5+nlines]) # Pull all the spectral data, the bulk of the mre file !!!Hard coded distance from the top of the file
    num_spectral_points = int(nlines/n_spec)
    for i in range(0,n_spec):
        wl = spec[i*num_spectral_points:(i*num_spectral_points+num_spectral_points),1]  # wavelength in microns
        R_meas = spec[i*num_spectral_points:(i*num_spectral_points+num_spectral_points),2] # Measured radiance (data)
        error = spec[i*num_spectral_points:(i*num_spectral_points+num_spectral_points),3] # error
        R_fit = spec[i*num_spectral_points:(i*num_spectral_points+num_spectral_points),5] # Fit radiance
        plt.fill_between(wl,R_meas+error,R_meas-error,color='lightgray')
        plt.plot(wl,R_meas,'black')
        plt.plot(wl,R_fit,'red')

chisq = reduced_chi_sq_finder(R_meas,error,R_fit)

# plot data and fit
plt.title('chisq/ny = '+str(chisq))
plt.ylabel('Radiance, nW/cm2/ster/micron')
plt.xlabel('Wavelength (microns)')
plt.legend(['Measured radiance','Fit radiance'])
plt.show()
