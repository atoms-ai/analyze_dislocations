# Dislocations
Codes to post process dislocation analysis files from ovito

Fortran codes for analysis of MD simulations<br />
<br />
Mostly used for meshing the paritcle-substrate simulation setup to compute pressure, temperature and other thermodyanmic properties<br />
<br />
- Dimensional analysis - Computes a real time particle height and width during deformation <br />
- Interface_PT - Computes the local pressure and temperatures for a thin region (user defined) at the particle/substrate interface<br />
- Analysis_2D_Pcorr - 2D meshing and bin-averaging the temperatures, pressures, velocities, etc for the whole system<br />
- automate_2D - Bash job script for running on multiple QCGD levels
