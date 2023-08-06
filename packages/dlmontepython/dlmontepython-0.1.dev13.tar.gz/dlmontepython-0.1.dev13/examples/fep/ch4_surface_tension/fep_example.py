# Uses the fep module to reweight a free energy profile obtained
# from a transition-matrix GCMC simulation (performed by DL_MONTE)
# near liquid-vapour coexistence to coexistence, and calculates
# various coexistence properties: the coexistence pressure and
# the liquid-vapour surface tension.

import dlmontepython.fep.fep as fep

# k_B*T used in simulation, units of kJ/mol
kt = 175 * 0.0083144621
# Value of ln(z) the simulation was performed at
lnz = -6.950
# Target ln(z) values for reweighting
lnz_target = [ -7.000, -6.900 ]
# Range of ln(z) to consider in search for coexistence
lnz_lbound = -7.0
lnz_ubound = -6.9
# Volume used in simulation (angstrom^3)
V = 30**3
# Molar mass of molecule (g/mol)
molarmass = 16.04
# Threshold between gas and liquid densities (g/ml):
# systems with densities < rho_thresh are considered a gas
rho_thresh = 0.17 

# Name of file containing free energy profile vs. number
# of molecules
filename = "FEDDAT.000_001"

# Import free energy profile over number of molecules
N, fe = fep.from_file(filename)

# Output the free energy profile over the density
rho = N * molarmass / (V * 0.60221409)
fep.to_file(rho, fe, "fep_vs_rho_"+str(lnz)+"_sim.dat")

# Reweight to target ln(z) and output
for lnz_new in lnz_target:
    fe_new = fep.reweight(N, fe, lnz, lnz_new)
    fep.to_file(rho, fe_new, "fep_vs_rho_"+str(lnz_new)+".dat")

# Locate coexistence ln(z) and output
N_thresh = rho_thresh * V * 0.60221409 / molarmass
lnz_co, p_co, fe_co = fep.reweight_to_coexistence(N, fe, lnz, lnz_lbound, lnz_ubound, N_thresh)
fep.to_file(rho, fe_co,  "fep_vs_rho_"+str(lnz_co)+"_co.dat")

# Calculate cooexistence pressure ((kJ/mol)/A^3)
pressure = fep.vapour_pressure(N, fe_co, N_thresh, kt, V)
print("coexistence pressure (bar) = ", pressure * 1E5 / 6.02214076)

# Calculate surface tension ((kJ/mol)/A^2)
tension = fep.surface_tension(N, fe_co, N_thresh, kt, V**(2.0/3.0) )
print("surface tension (N/m) = ", tension / 6.02214076)
