# author: Soumen Mohanty
# email: sm8966@nyu.edu
# version: 0.1 (19th December 2023)


# Command to test:-
# test single fastsurfer file
# python src/main.py --age 64 --sex F --stat-file data/aseg+DKT.stats --stat-type fastsurfer --normative-data data/normative_data.csv

# test both fastsurfer and samseg files
# python src/main.py --age 64 --sex F --stat-file data/aseg+DKT.stats --stat-type fastsurfer --stat-file data/samseg.stats --stat-type samseg --normative-data data/normative_data.csv

import argparse
from pipeline import run_pipeline
import os

class GlobalConfig:
    SAVE_INTERMEDIATE = True

def main():
    # Create an argument parser instance
    parser = argparse.ArgumentParser(description='CLI for the Stat Processing Pipeline. Converts .stat file(s) to a CSV and JSON for reporting.')

    # Arguments for the demographics of the subject
    parser.add_argument('--age', type=int, required=True, help='Age of the subject (years)')
    parser.add_argument('--sex', choices=['M', 'F'], required=True, help='Sex of the subject (M/F)')

    # Argument for the path to the stat files, can be used multiple times
    parser.add_argument('--stat-file', action='append', required=True, help='Path to a stat file')

    # Argument for the stat file type, can be used multiple times, defaults to 'fastsurfer'
    parser.add_argument('--stat-type', action='append', default=[], help='Type of stat file (fastsurfer or samseg)', choices=['fastsurfer', 'samseg'])

    # Required argument for the path to the normative data CSV
    parser.add_argument('--normative-data', required=True, help='Path to the normative data CSV')

    # Optional argument for the path to the configuration file, with a default value
    parser.add_argument('--config', default='src/config.json', help='Path to the configuration file')

    # Optional argument for the output directory, with a default value
    parser.add_argument('--output-dir', default='data/output', help='Directory to save the output CSV')

    # Optional flag argument to save intermediate dataframes
    parser.add_argument('--save-intermediate', action='store_true', help='Flag to save intermediate dataframes', default=True)

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Set environment variable
    os.environ['SAVE_INTERMEDIATE'] = '1' if args.save_intermediate else '0'

    # Ensuring each stat file has a corresponding type, defaulting to 'fastsurfer' if not specified
    stat_files = args.stat_file
    stat_types = args.stat_type + ['fastsurfer'] * (len(stat_files) - len(args.stat_type))

    # Run the pipeline with the processed arguments
    run_pipeline(args.age, args.sex, stat_files, stat_types, args.normative_data, args.config, args.output_dir)

if __name__ == '__main__':
    main()
