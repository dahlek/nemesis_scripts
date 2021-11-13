import os

def make_inputs(particle_sizes=[], cloud_params=[], haze_params=[], index=None):
    
    '''
    This program: 
    - Makes an .apr file assuming a Gaussian cloud and Gaussian haze (e.g. -1/-2 0 14)
    - Runs Makephase and makes the relevant scattering files
    - Basically makes input files and preps everything for Nemesis to be run
    - Associates the main cloud w/ aerosol profile #1, haze layer above it w/ aerosol profile #2
    - Assumes haze is made up of chromophore material (e.g. uses Carlson et al. 2016 for optical constants)
    - Assumes main cloud is ammonia-dominated
    
    Input:
    - particle_sizes = [r1, r2]
    - cloud_params/haze_params = [int. optical depth, optica depth error, altitude of peak (km), error on peak altitude (km), FWHM (km), error on FWHM (km)]
    
    Output:
    *.apr, *.xsc, hgphase*.dat, PHASE*.dat files
    
    To-do's:
    - Include model 444 (allow variance of haze complex n?)
    - Do we need to use Normxsc since we're not using model 227?
    - Vary gases?
    - Number of apr profiles currently hard-coded, apr profile just contains clouds
    
    Emma Dahl, Nov. 2021
    '''
    
    
    # Use particle sizes to define scattering properties w/ Makephase - - - - - - - - - -
    
    # Make file to normalize .xsc file (need to do this if using model 227):
    file = open('Normxsc_input','w')
    file.write('jupiter'+' \n')
    file.write('5 1'+' \n') # normalize the 6th wavelength (0.9) to 1
    file.close()
    
    # Make Makephase input
    number_of_inputmodels = '2'
    wavelength_or_wavenumber = '1' # 1 = wavelength
    rang = '1.55 2.325 0.025' # start, end, delta; what Rohini did
    name_of_xsc = 'jupiter'
    renormalize_phase_function = 'y'
    # aerosol 1, ammonia cloud
    calculation_type = '1'
    particle_a_and_b = str(particle_sizes[0])+' 0.1' # Assuming gamma distribution with b = 0.1
    size_int_param = '2' # 2 - use default
    ref_index = '4' # ammonia - this is what Kevin assumes
    # aerosol 2, haze
    calculation_type2 = '1'
    # if calculation_type = 1:
    particle_a_and_b2 = str(particle_sizes[1])+' 0.1'
    size_int_param2 = '2' # 2 - use default
    ref_index2 = '1' # constant value over range
    indexvalue2 = '1.4 0' # real index = 1.4, complex index = 0. a “typical value for aliphatic hydrocarbons” (Carlson et al. 2016)
    
    makephasename = 'makephase_input'

    # Save makephase input file
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
    file.write(ref_index2+'\n')
    file.write(indexvalue2 +' \n')
    file.close()
    
    os.system('rm *.xsc')
    # run makephase to make scattering files
    os.system('Makephase < '+makephasename)
    
    # Normalize with Normxsc and input file defined above loop (*might not need to do this?)
    os.system('Normxsc < Normxsc_input')
    
    # If running Nemesis over a particle size grid, save the necessary input files (assuming you have a directory for these inputs made already)
    #os.system('cp jupiter.xsc ./input/jupiter.xsc.'+str(index))
    #for i in range(int(n_aero_prof)):
    #    os.system('cp hgphase'+str(i+1)+'.dat  ./input/hgphase'+str(i+1)+'.dat.'+str(index))
    #    os.system('cp PHASE'+str(i+1)+'.dat  ./input/PHASE'+str(i+1)+'.dat.'+str(index))
    
    
    # Make .apr file - - - - - - - - - - - - - - - - - - - -
    # hard-coded here: number of profiles (2); just doing cloud profiles for now
    # From Nemesis manual, some notes by Emma:
    # Profile is a cloud with a specific density profile that has the shape of a Gaussian line. The profile is parameterised with in integrated optical depth, the altitude where the distribution peaks and the width of distribution in units of km. The next line of the .apr file then contains the a priori integrated optical depth and error, followed by the a priori altitude where the distribution peaks and the log width (e.g. FWHM) in km, with their respective errors. All quantities are taken as logs, except the altitude of the peak - that means the quantities you enter need to be >0, since NEMESIS takes the natural log of the values you enter later.
    
    file = open('jupiter.apr','w')
    
    file.write('******** any header info you like. One line only ******** \n')
    file.write(str(2)+'  ! number of variable profiles (vmr,T, or cont) \n')
    
    # Main cloud, Gaussian profile
    file.write('-1 0 14 \n')
    file.write(str(cloud_params[0])+' '+str(cloud_params[1])+'   ! total optical depth, error \n')
    file.write(str(cloud_params[2])+' '+str(cloud_params[3])+'   ! alt of peak (km), error \n')
    file.write(str(cloud_params[4])+' '+str(cloud_params[5])+'   ! FWHM (km), error \n')
    
    # Haze layer, Gaussian profile
    file.write('-2 0 14 \n')
    file.write(str(haze_params[0])+' '+str(haze_params[1])+'   ! total optical depth, error \n')
    file.write(str(haze_params[2])+' '+str(haze_params[3])+'   ! alt of peak (km), error \n')
    file.write(str(haze_params[4])+' '+str(haze_params[5])+'   ! FWHM (km), error \n')
    file.write('! Will appear at bottom of .mre file \n')
    
    file.close()
    
    
    #os.system('Nemesis < jupiter.nam > jupiter.log') # won't need bc running w/ submitjob.sh files on Gattaca
    # uncomment these if testing groups of cloud parameters:
    # os.system('cp jupiter.apr '+str(index)+'.jupiter.apr')
    
    
    
# Define input lists and run the program once
# cloud_params/haze_params = [int. optical depth, optica depth error, altitude of peak (km), error on peak altitude (km), FWHM (km), error on FWHM (km)]
# particle_sizes = [r1,r2]

particle_sizes = [0.1,0.2]
cloud1_params = [10,5,0.1,0.05,0.1,0.1]
cloud2_params = [1,0.5,30,15,0.1,0.1]

make_inputs(particle_sizes, cloud1_params, cloud2_params)


# Or, run it in a loop if you're testing multiple values; use the 4th input variable 'index' when you step forward bc it will append itself to the end of the multiple input files you'll generate
# e.g., you're running 5 different inputs for the a priori haze properties:
'''
for index in range(0,4):
    make_inputs(inputs1, inputs2, inputs3[index], index)
'''