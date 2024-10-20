#!/bin/bash


echo "Generate all plots for the analysis of parallel tool time and efficiency..."

# Store the current working directory
CURRENT_PWD=`pwd`

# Go to the performance folder
cd performance/

# Generate plots for parallel times and performance
chmod +x run_generate_tool_times_and_performance_plot.sh
./run_generate_tool_times_and_performance_plot.sh

# Go back to the previous working directory
cd ${CURRENT_PWD}

echo "All plots for the analysis of parallel times and efficiency have been generated."