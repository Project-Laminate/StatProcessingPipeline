import re
import pandas as pd
from scipy.stats import percentileofscore
import logging
import json
import os

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_stats_file(file_path):
    """
    Parses the .stat file and extracts the volume and structure name.

    :param file_path: Path to the .stat file
    :return: DataFrame with structure names as columns and their corresponding volumes
    """
    logging.info(f"Parsing .stat file: {file_path}")
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            split_line = re.split(r'\s+', line.strip())
            if len(split_line) < 5:
                continue
            volume_mm3 = split_line[3]
            struct_name = split_line[4]
            data.append([struct_name, volume_mm3])

    df = pd.DataFrame(data, columns=['StructName', 'Volume_mm3'])
    df['Volume_mm3'] = pd.to_numeric(df['Volume_mm3'], errors='coerce')

    # Transpose the DataFrame and set the first row as column headers
    df = df.T
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    return df

def clean_label(label):
    """
    Cleans the label by removing non-alphabetic characters and converting to lowercase.

    :param label: The label to clean
    :return: Cleaned label
    """
    return re.sub(r'[^a-zA-Z]', '', label).lower()

def create_new_columns(df, labels):
    """
    Sums up the volumes for specified structures and creates new columns for each hemisphere.

    :param df: The DataFrame with the original data
    :param labels: Dictionary with hemisphere labels and the corresponding brain structures
    :return: List of new column names created
    """
    logging.info("Creating new columns based on hemisphere labels")
    new_columns = []
    for region, components in labels.items():
        for hemisphere in ['rh', 'lh']:
            new_column_name = f"{clean_label(region)}_{hemisphere}"
            component_columns = [f"ctx-{hemisphere}-{clean_label(component)}" for component in components]
            existing_columns = [col for col in component_columns if col in df.columns]

            if existing_columns:
                df[new_column_name] = df[existing_columns].sum(axis=1)
                df[new_column_name] = df[new_column_name].round(3)
                new_columns.append(new_column_name)
            else:
                logging.warning(f"No columns found for {new_column_name}. Missing columns: {set(component_columns) - set(df.columns)}")
    
    return new_columns

def calculate_percentiles_and_normals(stats_df, normative_df, new_column_names):
    """
    Calculates percentiles and normal ranges for the given DataFrame and returns a DataFrame
    with only the new columns and their calculated values.

    :param stats_df: DataFrame with the statistics for a single patient
    :param normative_df: DataFrame with the normative data
    :param new_column_names: List of new column names to use for calculation
    :return: DataFrame with only the new columns and calculated percentile and normal range columns
    """
    logging.info("Calculating percentiles and normal ranges")
    new_data = {}
    for column in new_column_names:
        if column in stats_df.columns and column in normative_df.columns:
            value = stats_df[column].iloc[0]
            percentile = percentileofscore(normative_df[column], value, 'rank')
            max_normal = normative_df[column].mean() + (2 * normative_df[column].std())
            min_normal = normative_df[column].mean() - (2 * normative_df[column].std())

            new_data[f'{column}_volume'] = [value]
            new_data[f'{column}_percentile'] = [percentile]
            new_data[f'{column}_max_normal'] = [max_normal]
            new_data[f'{column}_min_normal'] = [min_normal]
        else:
            logging.warning(f"Column {column} not found in both stats_df and normative_df")

    return pd.DataFrame(new_data)


def create_other_columns(stats_df, normative_df, labels, columns_list):
    # parse through config['otherlabels'] and add the new columns to the DataFrame
    for label, components in labels.items():
        logging.info(f"Creating new column {components} based on {label}")
        # create a copy of the column labelled label and add it to the DataFrame with the new column name components
        stats_df[components] = stats_df[label]
        normative_df[components] = normative_df[label]

        columns_list.append(components)

    return columns_list

def csv_to_json(csv_path, json_path):
    """
    Converts CSV data to a structured JSON format, specifically designed for brain region metrics.

    The function assumes a CSV format where each column name is structured as 'region_hemisphere_metric',
    for example, 'frontal_lh_volume'. It processes these columns to create a nested JSON object
    with a hierarchy of region -> hemisphere -> metrics (volume, percentile, max, min).

    Parameters:
    csv_path (str): The file path of the source CSV file.
    json_path (str): The file path for the output JSON file.

    The function does not return any value. Instead, it writes the processed data to a JSON file.
    """
    
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Process and restructure the data
    report_data = {}
    for column in df.columns:
        parts = column.split('_')
        if len(parts) < 3:
            continue

        base_label = parts[0]
        hemisphere = parts[1]
        metric_type = parts[2]

        if base_label not in report_data:
            report_data[base_label] = {}

        if hemisphere not in report_data[base_label]:
            report_data[base_label][hemisphere] = {}

        metric_value = df[column].iloc[0]
        if metric_type == 'volume':
            report_data[base_label][hemisphere]['volume'] = metric_value
        elif metric_type == 'percentile':
            report_data[base_label][hemisphere]['percentile'] = metric_value
        elif metric_type == 'max':
            report_data[base_label][hemisphere]['max'] = metric_value
        elif metric_type == 'min':
            report_data[base_label][hemisphere]['min'] = metric_value

    # Save the processed data as JSON
    with open(json_path, 'w') as json_file:
        json.dump(report_data, json_file, indent=4)

