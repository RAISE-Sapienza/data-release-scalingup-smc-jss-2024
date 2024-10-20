#!/bin/bash

echo "Generate all plots for sample saving with the ensemble..."

CURRENT_PWD=`pwd`

cd ../../../
mkdir -p figures/samples/sample_saving
python code/generate_ensemble_sample_saving_plot.py --fcs-data data/case-studies/FCS/FCS_experiments_data_both_algo.json \
                                                    --at-data data/case-studies/AT/AT_experiments_data_both_algo.json \
                                                    --alma-data data/case-studies/ALMA/ALMA_experiments_data_both_algo.json \
                                                    -o figures/samples/sample_saving 2> /dev/null

cd ${CURRENT_PWD}

echo "Done."