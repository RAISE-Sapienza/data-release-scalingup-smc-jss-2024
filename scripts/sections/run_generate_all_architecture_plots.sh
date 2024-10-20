#!/bin/bash

echo "Generate all plots for the analysis of parallel architecture evaluation..."

# Store the current working directory
CURRENT_PWD=`pwd`

# Go to the architecture folder
cd architecture/

# Generate plot for production in linear scale
chmod +x run_generate_production_speed_plot_linear.sh
./run_generate_production_speed_plot_linear.sh

# Generate plot for sample production and consumption in log scale
chmod +x run_generate_production_consumption_speed_plot_log.sh
./run_generate_production_consumption_speed_plot_log.sh

# Go back to the previous working directory
cd ${CURRENT_PWD}


echo "All plots for the analysis of parallel architecture evaluation have been generated."
