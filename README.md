# Stat Processing Pipeline CLI

This project provides a command-line interface (CLI) for the Stat Processing Pipeline. It is designed to convert `.stat` files into CSV and JSON format using normative data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can check if Python is installed by running the following command in your terminal:

```sh
python --version

pip install -r requirements.txt
```

You also need to install the required Python packages. You can install them by running the following command in your terminal:

### Usage
You can use the CLI by running the following command in your terminal:

```sh
python src/main.py --stat-file data/aseg+DKT.stats --normative-data data/normative_data.csv
# Use the `--help` flag to see all available options
```

```sh
usage: main.py [-h] --stat-file STAT_FILE --normative-data NORMATIVE_DATA [--config CONFIG] [--output-dir OUTPUT_DIR]
               [--save-intermediate]

CLI for the Stat Processing Pipeline. Converts a .stat file to a CSV and JSON

optional arguments:
  -h, --help            show this help message and exit
  --stat-file STAT_FILE
                        Path to the .stat file
  --normative-data NORMATIVE_DATA
                        Path to the normative data CSV
  --config CONFIG       Path to the configuration file
  --output-dir OUTPUT_DIR
                        Directory to save the output CSV
  --save-intermediate   Flag to save intermediate dataframes
```

This command will convert the aseg+DKT.stats file into CSV and JSON format using the normative_data.csv file. The output files will be saved in the data/output directory.

_Note: /data contains sample .stat and normative data files._