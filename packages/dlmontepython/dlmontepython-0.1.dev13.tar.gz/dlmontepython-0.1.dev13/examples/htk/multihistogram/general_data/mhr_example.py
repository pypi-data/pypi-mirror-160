# Uses the htk.multihistogram module to apply multiple
# histogram reweighting to data obtained from three simulations
# (see below for details). The multiple histogram reweighting 
# is used to generate an isotherm: density vs. chemical potential.

import dlmontepython.htk.multihistogram as multihistogram
import numpy as np

# List of thermodynamic activities of the 3 simulations.
activities = [ 0.03337326996032608, 
               0.035673993347252395,
               0.038133326547045175 ]

# List of chemical potentials to calculate density at
# using reweighting
mu_target = np.linspace(-5.2,-4.8,20)

# Thermodynamic parameters common to all simulations
kT_sim = 1.5
V_sim = 8.0**3

# Arrays needed for reweight_observable_muvt function below
kT, mu, E, N, rho = ([] for i in range(0,5))

# Import data from simulation data files, which are assumed
# to be named 'E_a.dat' and 'N_a.dat', respectively, for files
# containing the energies and number of particles from a
# simulation at activity 'a'.
for activity_sim in activities:

    mu_sim =  np.log(activity_sim)*kT_sim

    kT.append(kT_sim)
    mu.append(mu_sim)

    E_sim = np.loadtxt("E_"+str(activity_sim)+".dat")
    N_sim = np.loadtxt("N_"+str(activity_sim)+".dat")
    rho_sim = N_sim / V_sim

    E.append(E_sim)
    N.append(N_sim)
    rho.append(rho_sim)

# Perform the reweighting and output
for mu_new in mu_target:
    
    rho_new = multihistogram.reweight_observable_muvt(
                kT, mu, E, N, rho, kT[0], mu_new)

    print(mu_new, rho_new)
    
