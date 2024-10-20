# Scaling Up Statistical Model Checking of Cyber-Physical Systems via Algorithm Ensemble and Parallel Simulations over HPC Infrastructures (raw data and plots) #

This repository contains raw data and code to generate all plots presented in the paper. 

*The software tool to verify safety/mission-critical systems through the approach presented in the paper is available upon request*.

## Structure 

This repository contains the following directories:

* `code` - folder containing the code used to generate each plot.
* `data` - folder containing the results of the experiments within JSON files.
* `figures` - folder containing all generated figures. 
* `scripts` - folder containing bash scripts to generate all plots.


## Running environment ##

To generate each plot, you need to configure a Python environment using Anaconda. To this end, you can follow the following instructions:

1. Install Anaconda (Miniconda in this setting) with Python 3.11.

2. Create a new environment with Anaconda and activate it as follows:
   ```
   conda create -n jss-scalingup-plots python=3.11
   conda activate jss-scalingup-plots
   ```

2. Install the Python packages within the requirements txt file. Run the command below:
    
    ```
    pip install -r requirements.txt
    ```

3. Install plotly-orca using anaconda with the following command:
    
    ```
    conda install -c plotly plotly-orca=1.3.1
    ```




## Generating Images ##

### Generate all images ###

To generate all images, run:

```
cd scripts/
chmod +x run_generate_all_plots.sh
./run_generate_all_plots.sh
```

### Sample size analysis

#### Generate all images about ensemble analysis in the sample size and sample saving ####

To generate all images about ensemble analysis in the sample size and sample saving, run:

```
cd scripts/sections/
chmod +x run_generate_all_samples_plots.sh
./run_generate_all_samples_plots.sh
```

#### Generate images about sample saving analysis ####

To generate all images about sample saving analysis, run:

```
cd scripts/sections/samples/
chmod +x run_generate_ensemble_sample_saving_plot.sh
./run_generate_ensemble_sample_saving_plot.sh
```

#### Generate images about sample size analysis ####

To generate all images about sample size analysis, run:

```
cd scripts/sections/samples/
chmod +x run_generate_ensemble_sample_size_plot.sh
./run_generate_ensemble_sample_size_plot.sh
```


### Architecture evaluation analysis ###

#### Generate all images about architecture evaluation analysis ####

To generate all images about architecture evaluation analysis, run:

```
cd scripts/sections/
chmod +x run_generate_all_architecture_plots.sh
./run_generate_all_architecture_plots.sh
```

#### Generate samples production-consumption rate in logarithmic scale image ####

To generate the image of the sample production-consumption rate using the logarithmic scale, run:

```
cd scripts/sections/architecture
chmod +x run_generate_production_consumption_speed_plot_log.sh
./run_generate_production_consumption_speed_plot_log.sh
```

#### Generate sample production rate in linear scale image ####

To generate the image of the sample production rate using the linear scale, run:

```
cd scripts/sections/architecture
chmod +x run_generate_production_speed_plot_linear.sh
./run_generate_production_speed_plot_linear.sh
```


### Parallel times and efficiency ###

#### Generate all images about parallel times and efficiency ####

To generate the image of parallel times and efficiency, run:

```
cd scripts/sections
chmod +x run_generate_all_performance_plots.sh
./run_generate_all_performance_plots.sh
```

## Authors ##

* Leonardo Picchiami ([picchiami@di.uniroma1.it](picchiami@di.uniroma1.it)) 
* Maxime Parmentier ([maxime.parmentier@uclouvain.be](maxime.parmentier@uclouvain.be))
* Axel Legay        ([axel.legay@uclouvain.be](axel.legay@uclouvain.be))
* Toni Mancini      ([tmancini@di.uniroma1.it](tmancini@di.uniroma1.it))
* Enrico Tronci     ([tronci@di.uniroma1.it](troncidi.uniroma1.it))
