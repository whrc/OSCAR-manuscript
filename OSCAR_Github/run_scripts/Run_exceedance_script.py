#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run OSCAR exceedance simulations (historical + scenario).

This script is intended as a template run_script for the OSCAR-manuscript
repository. Users will need to modify the paths in the SETUP section
to run a different parameter file or forcing set.

Created: 2025-06-10
Author: C. Schädel

"""

# ============================================================
# Imports
# ============================================================

import os
import sys

# ensure repo root is on python path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_root)

import re
import numpy as np
import xarray as xr


# import OSCAR
from core_fct.fct_process import OSCAR

# setup
# mod_region = 'RCP_5reg' # region configuration used when parameters were generated; not referenced directly here
model = OSCAR


# ============================================================
# paths to edit depending on the run
# ============================================================

# forcing files (historical + scenario)
folder_in = 'input_data/drivers/'

# parameter folder (contains the .nc parameter file(s))
folder_par = 'input_data/parameters/'

# output directory
folder_out = 'output_data/'


# Variables to save (choose your own)
varkeep = [
    'D_Tg', 'Eff', 'D_Eluc', 'D_Cfroz', 'D_Cthaw',
    'D_Epf_CO2', 'D_Epf_CH4', 
    'D_CO2_ab_pf', 'D_CH4_ab_pf',
    'D_Eburn_net_CO2','D_Eburn_net_CH4', 
    'D_FA_CO2', 'D_FA_CH4', 'D_Epf_CO2_fire', 'D_Epf_CH4_fire']


# ============================================================
# parameter file selection
# ============================================================

# change this filename to run a different parameter set
# expected pattern: Pars_<model>_500_<sim>.nc
# examples:
#   Pars_JSBACH_500_a.nc
#   Pars_JULES_DR_500_b.nc
#   Pars_ORCHIDEE_500_d.nc
file_path = os.path.join(folder_par, 'Pars_JSBACH_500_a.nc')

file_name = os.path.basename(file_path)
base_name, _ = os.path.splitext(file_name)
parts = base_name.split("_")

# model label inferred from filename (e.g. JULES_SR)
model_label = re.match(r"Pars_(.+?)_500_", file_name).group(1)

# simulation code inferred from parameter filename suffix (_a, _b, _c, _d)
sim_code = parts[-1]

simulation_step = f"{model_label}_{sim_code}"


# ============================================================
# load parameters and forcings
# ============================================================

Par_mc = xr.open_dataset(file_path)


# load forcing data for historical period
For_hist = xr.open_dataset(folder_in + 'For_hist_E_driven.nc')

# merge fixed (non-time-varying) variables from the forcing file into parameters
# OSCAR expects only time-dependent variables (with 'year') in the forcing dataset
Par_run = xr.merge([Par_mc, For_hist.drop_vars([VAR for VAR in For_hist if 'year' in For_hist[VAR].dims])])

# ensure required fire parameters exist even if fire is effectively off
if 'p_CO2_burn' not in Par_run:
    Par_run['p_CO2_burn'] = xr.DataArray(0.0, attrs={'units': '1'})
    
# ensure required fire parameters exist even if fire is effectively off
if 'p_CH4_burn' not in Par_run:
    Par_run['p_CH4_burn'] = xr.DataArray(0.0, attrs={'units': '1'})
    
    
# # keep only time-varying historical forcings
For_hist = For_hist.drop_vars([VAR for VAR in For_hist if 'year' not in For_hist[VAR].dims])

# load scenario forcing
For_scen = xr.open_dataset(folder_in + 'For_scen_E_driven.nc')

## drop any scenarios not used
For_scen = For_scen.drop_sel(scen=['SSP1-1.9', 'SSP3-7.0', 'SSP3-7.0-LowNTCF', 'SSP4-3.4', 'SSP5-3.4-OS'])

# select a time period for OSCAR to run
For_scen = For_scen.sel(year=slice(2014,2020))

# ============================================================
# initial conditions
# ============================================================

Ini_hist = xr.Dataset() 
for VAR in list(model.var_prog):
    if len(model[VAR].core_dims) == 0: 
        Ini_hist[VAR] = xr.DataArray(0.)
    else: Ini_hist[VAR] = sum([
        xr.zeros_like(Par_run[dim], dtype=float) if dim in Par_run.coords 
        else xr.zeros_like(For_hist[dim], dtype=float) for dim in model[VAR].core_dims
        ])

# ============================================================
# historical run, save output
# ============================================================

Out_hist = model(Ini_hist, Par_run, For_hist, var_keep = varkeep, nt = 2)

# save netcdf 
Out_hist.to_netcdf(folder_out + f"Out_hist_ex_E_{simulation_step}.nc", encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})

# ============================================================
# scenario run
# ============================================================

Ini_scen = Out_hist.sel(year=2014, drop = True)
Out_scen = model(Ini_scen, Par_run, For_scen, var_keep = varkeep, nt = 20)

# save Scenario run before weighting
Out_scen.to_netcdf(folder_out + f"Out_scen_exceedance_E_{simulation_step}.nc", encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_scen})


