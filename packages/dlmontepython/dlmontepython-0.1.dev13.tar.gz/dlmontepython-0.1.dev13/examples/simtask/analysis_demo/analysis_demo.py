# This script demonstrates how to use simtask.analysis to calculate the mean and
# standard error in data in a file 'energy.dat', by applying block averaging to the
# data after determining an equilibration time and rejecting data before 
# equilibration.

import dlmontepython.simtask.analysis as analysis
import numpy as np
import math

# Load data: 'energy.dat' contains energies output periodically during a simulation.
# The unit of time used here is the period between outputs to 'energy.dat'
data = np.loadtxt("energy.dat")

# Fractional distances along energy trajectory used as check points for 
# equilibration: 0, 0.2, 0.4, 0.6, 0.8
equilchecks = np.linspace(0.0, 1.0, num=5, endpoint=False)

# Check trajectory has equilibrated, and if so estimate the equlibration time 
isequilibrated, equiltime = analysis.equilibration_test(data, checktimes=equilchecks) 

if isequilibrated:

    print("Trajectory has equilibrated by time ", equiltime)
    
    corrtime = analysis.autocorrelation_time(data[equiltime:])
    print("Autocorrelation time = ", corrtime)

    # Use correlation time to inform block size in block averaging: We use a block
    # size 4 times the correlation time.
    blocksize = 4 * math.ceil(corrtime)

    # Calculate the mean energy E and standard error dE using block
    # averaging
    E, dE = analysis.standard_error(data[equiltime:], blocksize)

    print("Mean and standard error = ", E, dE)

else:

    print("Trajectory has not equilibrated")
