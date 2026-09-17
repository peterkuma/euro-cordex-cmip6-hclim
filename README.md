# Code for the manuscript “Evaluation of historical simulations in the HCLIM43-ALADIN regional climate downscaling ensemble over Europe in the EURO-CORDEX-CMIP6 framework”

This repository contains processing and plotting code for the manuscript
[Evaluation of historical simulations in the HCLIM43-ALADIN regional climate
downscaling ensemble over Europe in the EURO-CORDEX-CMIP6
framework](10.5281/zenodo.22813644). The results are presented in the
presentation [New ensemble of regional climate projections for
Europe](https://doi.org/10.5281/zenodo.20340840).

This code processes data from HCLIM43-ALADIN (a regional climate model, RCM)
downscaled simulations of a number of general circulation models (GCMs) and the
ERA5 reanalysis, observations from E-OBS, and the CERRA, CERRA-Land, and ERA5
reanalyses.

## Requirements

- GNU Parallel >= 20220722 (tested with 20220722)
- CDO >= 2.3.0 (tested with 2.3.0)
- wget (tested with 1.21.1)
- Python >= 3.14.2 (tested with 3.14.2)
- Python packages specified in `requirements.txt`

To install the Python packages, it is recommended to use a Python virtual
environment:

```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

This installs the precise version of the Python packages in order to maintain
reproducibility. Newer packages may be compatible as well, but this is untested.

You can leave the `venv` with `deactivate` and use it again with
`. venv/bin/activate`.

## Input data

Input data are required to be able to meaningfully use the code. These include
the global (CMIP6) and regional model (HCLIM) output, observations (E-OBS), and
reanalyses (CERRA and CERRA-Land). The paths to the source data are specified in
`sources/paths`. These should be changed to the actual paths on your system. The
HCLIM data are soon to be avaiable on the [Earth System Grid
Federation](https://esgf.github.io). The observations are reanalyes are publicly
available from the Copernicus Climate Change Service:
[E-OBS](https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php),
[CERRA](https://doi.org/10.24381/cds.622a565a),
[CERRA-Land](https://doi.org/10.24381/cds.a7f3cd0b), and
[ERA5](https://doi.org/10.24381/cds.143582cf).

The format of `sources/paths` is dataset name followed by input paths, separated
by space. `$freq`, `$var`, and `$stage` in the input paths are replaced with the
frequency (`day`, `mon`, or `yr`), variable name (such as `tas`), and stage name
(`core` or `tier1`), respectively. The paths should contain NetCDF files, one or
more files per variable, optionally split by time. The variables required for
the analysis are: `pr`, `psl`, `tas`, `tasmax`, and `tasmin`. The data for the
1991−2020 time period are patched together from the historical experiment
(1991−2014) and the SSP1-2.6 future projection (2015−2020). Therefore, the first
path of every line should point to the historical experiment files, and the
second path points to the SSP1-2.6 projection files.

There are four types of input data: the global CMIP6 model data (CNRM-ESM2-1,
EC-Earth3-Veg, IPSL-CM6A-LR, MIROC6, MPI-ESM1-2-HR, and NorESM2-MM); the HCLIM
regional model data; the E-OBS observations; and the CERRA, CERRA-Land, and ERA5
reanalyses. The global model data should be on a 1°×1° longitude−latitude grid
(GLB-1deg), and the rest on a European 12.5-km Lambert conformal conic
projection grid (EUR-12lcc). The CDO grid definitions of GLB-1deg and EUR-12lcc
are in `input/grid/GLB-1deg.txt` and `input/grid/EUR-12lcc.txt`, respectively.
The input files can be remapped to these grids using "`cdo
remapbil,input/grid/`*grid*`.txt` *input* *output*", where *grid* is `GLB-1deg`
or `EUR-12lcc`, *input* is the input NetCDF file and *output* is the output
NetCDF file. This step has to be done manually before filling the paths in
`sources/paths` (these should point to the re-gridded data). For the historical
evaluation manuscript, only monthly data are required.

## Usage

To run the processing and plotting code, the `./run TASK` script should be used,
where `TASK` is the task name. The following tasks are available:

```
source_links          Create source symlinks in the input directory.
remap_landmask        Remap land mask to a 1x1 degree grid for GCM calculations.
remap_obs             Remap observatiosn to a 1x1 degree grid for GCM calculations.
calc_ensembles        Calculate model ensembles.
calc_stats            Calculate statistics (dep: source_links, remap_landmask, remap_obs, ensemble).
calc_clim_indices     Calculate climate indices.
calc_model_ranking    Calculate model ranking (dep: calc_stats).
plot_map_mean         Plot maps for means (dep: calc_stats).
plot_map_diff         Plot maps for differences between time periods (dep: calc_stats).
plot_map_trend        Plot maps for linear trends (dep: calc_stats).
plot_heatmap_mean     Plot heatmaps for means (dep: calc_stats).
plot_heatmap_diff     Plot heatmaps for differences between time periods (dep: calc_stats).
plot_heatmap_trend    Plot heatmaps for trends (dep: calc_stats).
plot_boxplot          Plot boxplots with statistics (dep: calc_stats).
plot_gcm_rcm_scatter  Plot GCM-RCM scatter plot for temperature and precipitation (dep: calc_stats).
plot_model_ranking    Plot model ranking (dep: model_ranking).
plot_timeseries       Plot time series (dep: calc_stats).
plot_annual_cycle     Plot annual cycle (dep: calc_stats).
plot_gcm_rcm_tas      Plot GCM. vs RCM. temperature change.
download_topo         Download topography.
remap_topo            Remap topography (dep: download_topo).
plot_domain_map       Plot domain map (dep: remap_topo).
archive               Prepare an archive of input data.
```

The individual processing and plotting commands are under `bin`. To see help
for a command, run it without any arguments, e.g., `bin/calc_stats`.

The `run` script and the command should always be run from the main directory of
this repository.

## Releases

### 1.0.0 (2026-09-17)

- Initial release for the submitted manuscript.

## License

The code has been developed by Peter Kuma and is available under the terms of
the MIT license (see `LICENSE.md`).
