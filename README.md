# OSCAR abrupt postfire repository

This repository contains the scripts and input files used to run OSCAR v3.0, a compact Earth System Model, for the analyses presented in 

**Schädel, C.**, Gasser, T., Rogers, B.M., Treharne, R., Turetsky, M.R., Smith, T., MacDonald, E., and Natali, S.M. (2026). Permafrost and wildfire carbon emissions indicate need for additional action to keep Paris Agreement temperature goals within reach. *Commun. Earth Environ.* https://doi.org/10.1038/s43247-026-03189-5

OSCAR is maintained at: https://github.com/tgasser/OSCAR 
The OSCAR framework is documented in Gasser et al. (2017, 2018).

## Model extensions

This version extends OSCAR v3.0 to simulate:
- abrupt permafrost thaw,
- below-ground carbon combustion from high-latitude fires
- post-fire permafrost thaw emissions

## Repository structure

**core_fct/**

  Core OSCAR model code. New permafrost and fire modules are implemented in `fct_process.py` (Section 1.4: Permafrost)

**input_data/**
Model input files
- **drivers/**: historical and scenario forcing files
- **parameters/**: parameter files defining specific model configurations


**run_scripts/**

Example run script used to generate the simulations in the manuscript. 


**output_data/**  

Processed output data used to generate the figures and tables in the manuscript  
(CSV format; aggregated and post-processed model results)

## Parameter files
  Parameter files follow the pattern:

  Pars_<model>_500_<sim>.nc

  where:

- `<model>` is the land surface model used to calibrate the gradual thaw emulator (e.g. JSBACH, JULES_DR, ORCHIDEE)
- `500` denotes the number of Monte-Carlo parameter configurations
- `<sim>` denotes the permafrost configuration:
  - `a`: gradual thaw only 
  - `b`: gradual + abrupt thaw 
  - `c`: gradual + abrupt thaw + combustion
  - `d`: gradual + abrupt thaw + combustion + post-fire thaw
 

## References

1. Gasser et al. (2017). *The compact Earth system model OSCAR v2.2: description and first results*.  
   [https://doi.org/10.1038/ngeo3031](https://doi.org/10.5194/gmd-10-271-2017)

2. Gasser et al. (2018). *Path-dependent reductions in CO2 emission budgets caused by permafrost carbon release*.  
   [https://doi.org/10.1038/s41561-018-0227-0](https://doi.org/10.1038/s41561-018-0227-0)
