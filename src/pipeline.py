import os
import pandas as pd
import json
from utils import create_other_columns, csv_to_json, parse_stats_file, create_new_columns, calculate_percentiles_and_normals
import logging

def run_pipeline(stat_file_path, normative_data_path, config_path, output_dir, save_intermediate):
    # Ensure the output and intermediate directories exist
    os.makedirs(output_dir, exist_ok=True)
    intermediate_dir = os.path.join(output_dir, 'intermediate')
    os.makedirs(intermediate_dir, exist_ok=True)
    
    # Load the hemisphere labels configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    # Process the .stat file to extract the data and transform it into a DataFrame
    stats_df = parse_stats_file(stat_file_path)
    
    # If the user wants to save the intermediate results
    if save_intermediate:
        intermediate_stats_path = os.path.join(intermediate_dir, 'parsed_stats.csv')
        stats_df.to_csv(intermediate_stats_path, index=False)
        logging.info(f'Parsed stats saved to {intermediate_stats_path}')

    # Load normative data
    normative_df = pd.read_csv(normative_data_path)
    
    
    # Create new columns and get the list of new column names
    stats_new_column_names = create_new_columns(stats_df, config['additions']['hemisphere_labels'])
    logging.info(f'New column names in stats: {stats_new_column_names}')

    normative_new_column_names = create_new_columns(normative_df, config['additions']['hemisphere_labels'])
    logging.info(f'New column names in normative data: {normative_new_column_names}')

    stats_new_column_names = create_other_columns(stats_df, normative_df, config['otherlabels'], stats_new_column_names)

    # #  check if the new column names are the same in both DataFrames
    # if stats_new_column_names != normative_new_column_names:
    #     raise ValueError("New column names are not the same in both DataFrames")

    # Calculate percentiles and normal ranges using the new column names
    final_df = calculate_percentiles_and_normals(stats_df, normative_df, stats_new_column_names)

    # Save the final DataFrame as a CSV file
    final_output_path = os.path.join(output_dir, 'final_report.csv')
    final_df.to_csv(final_output_path, index=False)
    logging.info(f'Final report saved to {final_output_path}')

    # Save the final DataFrame as a JSON file
    json_output_path = os.path.join(output_dir, 'final_report.json')
    csv_to_json(final_output_path, json_output_path)
    logging.info(f'JSON report saved to {json_output_path}')

# You can call run_pipeline here for testing or you can use this module as an import.
