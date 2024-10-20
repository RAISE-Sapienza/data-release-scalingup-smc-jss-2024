#!/bin/bash


echo "Generate plot for sample production rate in linear scale..."

cd ../../../
mkdir -p figures/architecture/
python code/generate_production_speed_plot_linear.py --exp-data data/architecture/architecture_evaluation.json \
                                                     --output figures/architecture/parallel_prod_speed_eval_linear.pdf 2> /dev/null

echo "Done."