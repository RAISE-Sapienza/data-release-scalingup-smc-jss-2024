#!/bin/bash

echo "Generate all plots..."

# Store the current working directory
CURRENT_PWD=`pwd`

# Go to the sections folder
cd sections/

# Generate plots for ensemble analysis on samples
chmod +x run_generate_all_samples_plots.sh
./run_generate_all_samples_plots.sh

# Generate plots for parallel architecture evaluation
chmod +x run_generate_all_architecture_plots.sh
./run_generate_all_architecture_plots.sh

# Generate plots for parallel times and efficiency
chmod +x run_generate_all_performance_plots.sh
./run_generate_all_performance_plots.sh

# Go back to the starting current directory folder
cd ${CURRENT_PWD}


echo "All plots have been generated."