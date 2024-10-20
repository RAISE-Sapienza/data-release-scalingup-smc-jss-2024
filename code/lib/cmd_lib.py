import argparse as arg


def get_command_line():
    parser = arg.ArgumentParser(description="Process all optimisation log file")

    parser.add_argument('--exp-data', type=str, dest='experiment_data',
                        help="The folder of the experiments",
                        required=True)

    parser.add_argument('--output', '-o', type=str, dest='output',
                        help="Path of the experiments seeds",
                        required=True)

    arguments = parser.parse_args()

    return arguments.experiment_data, arguments.output


def get_command_line_plots():
    parser = arg.ArgumentParser(description="Process all optimisation log file")

    parser.add_argument('--fcs-data', type=str, dest='FCS_data',
                        help="The folder of the experiments",
                        required=True)

    parser.add_argument('--at-data', type=str, dest='AT_data',
                        help="The folder of the experiments",
                        required=True)

    parser.add_argument('--alma-data', type=str, dest='ALMA_data',
                        help="The folder of the experiments",
                        required=True)

    parser.add_argument('--output', '-o', type=str, dest='output',
                        help="Path of the experiments seeds",
                        required=True)

    arguments = parser.parse_args()

    return arguments.FCS_data, arguments.AT_data, arguments.ALMA_data, arguments.output