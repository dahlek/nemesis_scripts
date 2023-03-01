Python scripts I frequently use to run NEMESIS or analyze results. (everything's in python 2.7!)

mre_reader.py - plots measured spectra and error, and fitted synthetic spectrum, as reported by the *.mre file. (I have other mre readers that will plot additional subplots for multiple spectra - let me know if you'd like to use that, happy to share)

aerosol_reader.py - plots the aerosol profile(s) from aerosol.prf

nem_CB_wrapper.py - calls various NEMESIS routines to develop Creme Brulee models

fcloud_maker.py - makes a new fcloud.ref file; helpful after using Profile to reconfigure pressure levels
