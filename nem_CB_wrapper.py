# ammonium hydrosulfide lookup table doesn't work for our wavelengths - add constant complex n spectrum for now from https://www.researchgate.net/publication/249341931_Optical_constant_of_ammonium_hydrosulfide_ice_and_ammonia_ice
# Specifically written for making Creme Brulee models; runs Makephase, Normxsc, and Dust_profile (not necessary if using 227 0 227 in .apr file)
# run final call at end of file in a loop to complete grid searches for particle size or other parameters
# WARNING: lots of hard-coded junk abounds herein; proceed with caution if you're not using this specifically for CB modeling in the optical

import numpy as np
import os
from scipy import interpolate
import math

def input_maker(apr_percent_error1, r1, r2, r3, tau_1, tau_2, tau_3, P_mc_base, P_mc_top, index, num_of_apr_profiles):
    
    '''
    Makes/deals with all files associated with particle size, color, and scattering (.xsc, PHASE*.dat,hgphase*.dat,cloud2.dat,refindex). Assumes all input pressures are in bar.
    Fractional errors for model 227 that are hard-coded: fsh, stratospheric haze optical depth and haze, ammonia scale factor
    Error for parameters in cloud2.dat are also hard-coded.
    
    Variables:
    Cloud 1 - MC in CB model
    Cloud 2 - Chromophore layer in CB model
    Cloud 3 - SH in CB model
    apr_percent_error - applied to variables in CB model in .apr file
    r* - particle sizes (microns)
    tau_* - optical depth of cloud
    P_mc_base - Base pressure of MC in CB model (bar)
    P_mc_top - Top pressure of MC in CB model (bar)
    index - used in previous iteration of this program. can be used when saving multiple output/input files.
    num_of_apr_profiles - Number of profiles that will appear at top of .apr file. 1st two profiles are 227 and the density factor for the deep sheet cloud, then ammonia scaling factor, then complex n spectrum of chromophore.
    '''
    
    # assumes inputs are in bar!!! will convert pressures from bar to atm
    atm_per_bar = 0.986923
    P_mc_base *= atm_per_bar
    P_mc_top *= atm_per_bar
    
    # Make file to normalize .xsc file (need to do this if using model 227):
    file = open('Normxsc_input','w')
    file.write('jupiter'+' \n')
    file.write('10 1'+' \n') # normalize the 10th wavelength (0.9) to 1
    file.close()
    
    # - - - - - - - - - - - - - - - - - - - - -
    
    # Make .xsc input, run Makephase:
    
    number_of_inputmodels = '3'
    wavelength_or_wavenumber = '1' # 1 = wavelength
    rang = '0.45 1.0 0.05' # start, end, delta
    name_of_xsc = 'jupiter'
    renormalize_phase_function = 'y'

    # 1, ammonia cloud
    calculation_type = '1'
    particle_a_and_b = str(r1)+' 0.1' # r1[i] is the main cloud's particle size. Assuming gamma distribution with b = 0.1
    size_int_param = '2' # 2 - use default
    ref_index = '4' # ammonia - this is what Kevin assumes

    # 2, chromophore
    calculation_type2 = '1'
    # if calculation_type = 1:
    particle_a_and_b2 = str(r2)+' 0.1'
    size_int_param2 = '2' # 2 - use default
    ref_index2 = '11' # read external look-up table
    # will print this at the end, since makephase asks for it at the end 
    name_of_table2 = 'refindex' # make refindex table in Desktop/nemesis_inputs_march2019/sromovsky_chromophore_data/carlson_chromophore.ipynb, or pull info from top of this notebook

    # 3, haze layer
    calculation_type3 = '1' # mie scatteirng, gamma distribution
    particle_a_and_b3 = str(r3)+' 0.1'
    size_int_param3 = '2' # 2 - use default
    ref_index3 = '1' # constant value over range
    indexvalue3 = '1.4 0' # real index = 1.4, complex index = 0

    makephasename = 'makephase_input'

    # Save makephase file
    file = open(makephasename,'w')
    # preamble stuff
    file.write(number_of_inputmodels+' \n')
    file.write(wavelength_or_wavenumber+' \n')
    file.write(rang+' \n')
    file.write(name_of_xsc+' \n')
    file.write(renormalize_phase_function+' \n')
    # Cloud 1
    file.write(calculation_type+' \n')
    file.write(particle_a_and_b+' \n')
    file.write(size_int_param+' \n')
    file.write(ref_index+' \n')
    # Cloud 2
    file.write(calculation_type2+' \n')
    file.write(particle_a_and_b2+' \n')
    file.write(size_int_param2+' \n')
    file.write(ref_index2+' \n')
    # Cloud 3
    file.write(calculation_type3+'\n')
    file.write(particle_a_and_b3+'\n')
    file.write(size_int_param3+'\n')
    file.write(ref_index3+'\n')
    file.write(indexvalue3 +' \n')
    # Name of refindex lookup table for chromophore (asks for at end for some reason)
    file.write(name_of_table2+' \n')
    file.close()

    os.system('rm *.xsc')
    # run makephase to make scattering files
    os.system('Makephase < '+makephasename)

    # Normalize with Normxsc and input file defined above loop
    os.system('Normxsc < Normxsc_input')
    
    # If doing multiple runs, uncomment these:
    #os.system('cp jupiter.xsc ./input/jupiter.xsc.'+str(index))
    #os.system('cp hgphase1.dat  ./input/hgphase1.dat.'+str(index))
    #os.system('cp hgphase2.dat  ./input/hgphase2.dat.'+str(index))
    #os.system('cp hgphase3.dat  ./input/hgphase3.dat.'+str(index))
    #os.system('cp hgphase4.dat  ./input/hgphase4.dat.'+str(index))
    #os.system('cp PHASE1.DAT  ./input/PHASE1.DAT.'+str(index))
    #os.system('cp PHASE2.DAT  ./input/PHASE2.DAT.'+str(index))
    #os.system('cp PHASE3.DAT  ./input/PHASE3.DAT.'+str(index))
    #os.system('cp PHASE4.DAT  ./input/PHASE4.DAT.'+str(index))
    
    
    # - - - - - - - - - - - - - - - - - - - - -
    
    
    # Change cloud2.dat based on chromophore size.
    # Original file was made in Desktop/nemesis_inputs_march2019/sromovsky_chromophore_data/carlson_chromophore.ipynb. Format described in manual.
    
    # Read in complex n spectrum from Carlson et al. 2016:
    complexn = np.loadtxt('/Users/dahlek/Desktop/nemesis_inputs_march2019/sromovsky_chromophore_data/complex_n',delimiter=',')
    complex_func = interpolate.interp1d(complexn[:,0],complexn[:,1])
    
    particle_size = r2 
    particle_size_error = 1e-8
    particle_size_variance = 0.1 # gamma dist
    particle_size_variance_error = 1e-8

    spectrum_error = 0.2 # ashwin used 20%
    correlation_length = 1.5 # based on what Rohini told me in 2018 (supposedly the "golden number" for correlation length, not sure what the units are.

    num_points=12
    wl_interp = np.linspace(0.45,1.0,num_points)
    
    file = open('cloud2.dat','w')
    
    file.write(str(particle_size)+' '+str(particle_size_error)+' \n')
    file.write(str(particle_size_variance)+' '+str(particle_size_variance_error)+' \n')
    file.write(str(num_points)+' '+str(correlation_length)+' \n')
    file.write('0.9 1.4 \n')
    file.write('0.9 \n')
    
    for i in range(0,len(wl_interp)):
        file.write( str(round(wl_interp[i],5))+' '+str(round(complex_func(wl_interp[i]),5))+' '+ str(round(round(complex_func(wl_interp[i]),5)*spectrum_error,5))+' \n' )
    file.close()
    
    #os.system('cp cloud2.dat ./input/'+str(index)+'.cloud2.dat')
    
    
    
    # - - - - - - - - - - - - - - - - - - - - -

    # Use Dust_profile to make the deep sheet cloud
    
    # Open .xsc file to get x-section at the wavelength where you want the required optical depth (0.9 microns)
    
    
    # pull info for dust_profile_input:
    xsc = './jupiter.xsc' 
    
    cloud_option = '4'
    base_top_scaleheight = str(round(P_mc_base,5))+' '+str(round(P_mc_top,5))+' 1.0'
    optical_depth_error = str(tau_1)+' '+str(round(P_mc_base,5)+1) # average optical depth from sromovsky results

    xsc = './jupiter.xsc' # for work computer
    #xsc = '/Users/dahlek/Desktop/nemesis_test1/jupiter.xsc' # for tests on laptop
    with open(xsc,'r') as f:
        all_data=[x.split() for x in f.readlines()]
        for p in range(1,len(all_data)):
            if round(float(all_data[p][0]),2) == 0.9:
                cross_section = float(all_data[p][1])
    cross_section_and_wavelength = str(cross_section)+' 1.00'


    # Chromophore
    cloud_option2 = '4'
    base_top_scaleheight2 = str(round(P_mc_top,5))+' '+str(round(P_mc_top*0.9,5))+' 1.0' # need to base these off main cloud
    optical_depth_error2 = str(tau_2)+' '+str(round(P_mc_top,5)+1)

    with open(xsc,'r') as f:
        all_data=[x.split() for x in f.readlines()]
        for p in range(1,len(all_data)):
            if round(float(all_data[p][0]),2) == 0.9:
                cross_section2 = float(all_data[p][2])
    cross_section_and_wavelength2 = str(cross_section2)+' 1.00'

    # stratospheric haze
    cloud_option3 = '4'
    base_top_scaleheight3 = '0.01 0.009 1'
    optical_depth_int = '0.001 0.5'

    with open(xsc,'r') as f:
        all_data=[x.split() for x in f.readlines()]
        for p in range(1,len(all_data)):
            if round(float(all_data[p][0]),2) == 0.9:
                cross_section3 = float(all_data[p][3])
    
    # write dust profile input file
    file = open('Dust_profile_input','w')
    file.write('jupiter \n')
    file.write('aerosol \n')
    file.write('3 \n') # number of particle types
    # CB MC
    file.write(cloud_option+' \n')
    file.write(base_top_scaleheight+' \n')
    file.write(optical_depth_error+' \n')
    file.write(cross_section_and_wavelength+' \n')
    # CB chromo
    file.write(cloud_option2+' \n')
    file.write(base_top_scaleheight2+' \n')
    file.write(optical_depth_error2+' \n')
    file.write(cross_section_and_wavelength2+' \n')
    # CB strato
    file.write(cloud_option3+' \n')
    file.write(base_top_scaleheight3+' \n')
    file.write(optical_depth_int+' \n')
    file.write(str(cross_section3)+' \n')

    file.close()
    
    os.system('Dust_profile < Dust_profile_input')
    os.system('cp aerosol.prf aerosol.ref')
    
    
    
    # - - - - - - - - - - - - - - - - - - - - -
    
    # Make .apr file
    
    file = open('jupiter.apr','w')

    file.write('******** any header info you like. One line only ******** \n')
    file.write(str(num_of_apr_profiles)+'                       ! number of variable profiles (vmr,T, or cont) \n')

    # CB clouds:
    file.write('227 0 227 \n')
    file.write(str(round(P_mc_base,4))+' '+str(round(P_mc_base*apr_percent_error1,3))+' ! main cloud base presure \n')
    file.write(str(round(tau_1,4))+' '+str(round(tau_1*apr_percent_error1,3))+' ! main cloud opacity \n')
    file.write('1.0 1e-8         ! main cloud frac. scale height \n')
    file.write(str(round(P_mc_top,4))+' '+str(round(P_mc_top*apr_percent_error1,4))+'   ! chromophore base \n')
    file.write(str(round(tau_2,4))+' '+str(round(tau_2*apr_percent_error1,4))+'     ! chromophore optical depth \n')
    file.write('0.01 0.0025      ! stratosphere base \n') 
    file.write('0.01 0.0025     ! stratosphere opt \n')
    file.write('0              ! 0 -> 0.9xtop pressure \n')
    
    # ammonia
    file.write('11 0 3 \n')
    file.write('1.0 0.25 \n')

    # complex n of chromophore
    file.write('444 2 444 \n')
    file.write('cloud2.dat \n')
    file.write('! Will appear at bottom of .mre file \n')
    file.close()

    os.system('Nemesis < jupiter.nam > jupiter.log')
    #os.system('cp jupiter.apr '+str(index)+'.jupiter.apr')    
    #os.system('cp jupiter.mre '+str(index)+'.jupiter.mre')

    
    
# Run it:
apr_percent_error = 0.2

# EZ
# put pressures in bar!!!
tau_1_solution = 13.663 # MC optical depth
tau_2_solution = 0.05 # Chromophore optical depth
tau_3_solution = 0.01
P_mc_base_solution = 2.154 # Bottom of main cloud (bar)
P_mc_top_solution = 0.05 # Top of main cloud/Bottom of chromophore layer (bar)

r_1 = 0.75
r_2 = 0.1
r_3 = 0.1

i = 1

apr_profiles = 1

input_maker(apr_percent_error, r_1, r_2, r_3, tau_1_solution, tau_2_solution, tau_3_solution, P_mc_base_solution, P_mc_top_solution, i, apr_profiles)
