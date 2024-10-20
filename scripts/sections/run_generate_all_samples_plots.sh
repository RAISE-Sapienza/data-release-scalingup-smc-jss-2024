#!/bin/bash

echo "Generate all plots for the analysis of samples..."

# Store the current working directory
CURRENT_PWD=`pwd`

# Go to the samples folder
cd samples/

# Generate plots for samples saving with the ensemble
chmod +x run_generate_ensemble_sample_saving_plot.sh
./run_generate_ensemble_sample_saving_plot.sh

# Generate plots for sample size taken by the ensemble
chmod +x run_generate_ensemble_sample_size_plot.sh
./run_generate_ensemble_sample_size_plot.sh

# Go back to the initial working directory
cd ${CURRENT_PWD}

echo "All plots for the analysis of samples have been generated."