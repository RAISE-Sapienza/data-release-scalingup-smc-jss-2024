#!/bin/bash

echo "Generate all plots for parallel times and efficiency..."

cd ../../../
mkdir -p figures/performance/AT
mkdir -p figures/performance/FCS
mkdir -p figures/performance/ALMA
python code/generate_tool_times_and_performance_plot.py --fcs-data data/case-studies/FCS/FCS_experiments_data_performance.json \
                                                   --at-data data/case-studies/AT/AT_experiments_data_performance.json \
                                                   --alma-data data/case-studies/ALMA/ALMA_experiments_data_performance.json \
                                                   -o figures/performance/ 2> /dev/null

echo "Done."