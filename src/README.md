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

This command will convert the aseg+DKT.stats file into CSV and JSON format using the normative_data.csv file. The output files will be saved in the data/output directory.
