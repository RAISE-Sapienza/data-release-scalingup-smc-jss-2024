#!/bin/bash

echo "Generate plot for sample production and consumption rate in linear scale..."


cd ../../../
mkdir -p figures/architecture/
python code/generate_production_consumption_speed_plot_log.py --exp-data data/architecture/architecture_evaluation.json \
                                                              --output figures/architecture/parallel_prod_cons_speed_eval_log.pdf 2> /dev/null

echo "Done."