import os
import pandas as pd
import json
from utils import (create_other_columns, csv_to_json, parse_fastsurfer_stats_file, 
                   parse_samseg_stats_file, create_new_columns, calculate_percentiles_and_normals,
                   save_combined_stats_df, new_stats_df, new_normative_df, reorder_json)
import logging

def run_pipeline(age, sex, stat_file_paths, stat_types, normative_data_path, config_path, output_dir):
    # Ensure the output and intermediate directories exist
    os.makedirs(output_dir, exist_ok=True)
    intermediate_dir = os.path.join(output_dir, 'intermediate')
    os.makedirs(intermediate_dir, exist_ok=True)
    
    # Load the hemisphere labels configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Initialize an empty DataFrame for stats
    combined_stats_df = pd.DataFrame()

    for stat_file_path, stat_type in zip(stat_file_paths, stat_types):
        if stat_type == 'fastsurfer':
            stats_df = parse_fastsurfer_stats_file(stat_file_path)
            fastsurfer_path = stat_file_path
        elif stat_type == 'samseg':
            stats_df = parse_samseg_stats_file(stat_file_path)
        
        # Check and exclude columns that already exist in combined_stats_df
        new_columns = stats_df.columns.difference(combined_stats_df.columns)
        # Combine data from different stat files
        combined_stats_df = pd.concat([combined_stats_df, stats_df[new_columns]], axis=1)

        _ = save_combined_stats_df(combined_stats_df)

        ###x Continue working with combined stats from here

    # clear the stats_df variable
    stats_df = None
    stats_df = parse_fastsurfer_stats_file(fastsurfer_path)

    # # Process the .stat file to extract the data and transform it into a DataFrame
    stats_df['Sex'] = sex  # 'sex' from the command-line argument
    stats_df['Age'] = age  # 'age' from the command-line argument

    # Load normative data
    normative_df = pd.read_csv(normative_data_path)
    
    # Create new columns and get the list of new column names
    stats_new_column_names = create_new_columns(stats_df, config['additions']['hemisphere_labels'])
    logging.info(f'New column names in stats: {stats_new_column_names}')

    normative_new_column_names = create_new_columns(normative_df, config['additions']['hemisphere_labels'])
    logging.info(f'New column names in normative data: {normative_new_column_names}')

    stats_new_column_names = create_other_columns(stats_df, normative_df, config['otherlabels'], stats_new_column_names)

    # save the new stats and normative dataframes as intermediate files
    _ = new_stats_df(stats_df)
    _ = new_normative_df(normative_df)

    # Calculate percentiles and normal ranges using the new column names
    final_df = calculate_percentiles_and_normals(stats_df, normative_df, stats_new_column_names)

    # # Save the final DataFrame as a CSV file
    final_output_path = os.path.join(output_dir, 'final_report.csv')
    final_df.to_csv(final_output_path, index=False)
    logging.info(f'Final report saved to {final_output_path}')

    # Save the final DataFrame as a JSON file
    json_output_path = os.path.join(output_dir, 'final_report.json')
    csv_to_json(final_output_path, json_output_path)
    logging.info(f'JSON report saved to {json_output_path}')

    reordered_json_output_path = os.path.join(output_dir, 'reordered_final_report.json')
    reorder_json(json_output_path, reordered_json_output_path)

# You can call run_pipeline here for testing or you can use this module as an import.
