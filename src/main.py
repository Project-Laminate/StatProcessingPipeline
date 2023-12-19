# author: Soumen Mohanty
# email: sm8966@nyu.edu
# version: 0.1 (19th December 2023)


# Command to test: 
# python main.py --stat-file ../data/aseg+DKT.stats --normative-data ../data/normative_data.csv

import argparse
from pipeline import run_pipeline

def main():
    # Create an argument parser instance
    parser = argparse.ArgumentParser(description='CLI for the Stat Processing Pipeline. Converts a .stat file to a CSV and JSON')

    # Required argument for the path to the .stat file
    parser.add_argument('--stat-file', required=True, help='Path to the .stat file')

    # Required argument for the path to the normative data CSV
    parser.add_argument('--normative-data', required=True, help='Path to the normative data CSV')

    # Optional argument for the path to the configuration file, with a default value
    parser.add_argument('--config', default='config.json', help='Path to the configuration file')

    # Optional argument for the output directory, with a default value
    parser.add_argument('--output-dir', default='../data/output', help='Directory to save the output CSV')

    # Optional flag argument to save intermediate dataframes
    parser.add_argument('--save-intermediate', action='store_true', help='Flag to save intermediate dataframes', default=True)

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Run the pipeline with the provided arguments
    run_pipeline(args.stat_file, args.normative_data, args.config, args.output_dir, args.save_intermediate)

# This conditional is used to ensure the script can be imported without running the main function,
# but will run main if the script is executed through the command line
if __name__ == '__main__':
    main()
