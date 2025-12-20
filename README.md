# cleaning_data
CSV Data Cleaning & Conversion Pipeline

#Overview

This repository contains a simple, modular data-processing pipeline for cleaning raw CSV data and converting the cleaned output into Excel format. The pipeline is designed to be interactive, transparent, and easy to run from the command line.

# Pipeline Flow

Raw CSV → Data Cleaning (CLI) → Cleaned CSV → CSV to Excel Conversion → Excel File

# Scripts

# clean_data.py

An interactive command-line tool for cleaning CSV datasets using configurable cleaning profiles.

Features
	•	Prompts for input CSV file
	•	Profile-driven cleaning logic:
	•	Standard: trims whitespace, removes duplicates, fills missing numeric values with median, fills missing text values with mode or "N/A"
	•	Aggressive: trims whitespace, removes duplicates, fills missing numeric values with 0, fills missing text values with "N/A", drops fully empty rows
	•	Logs all cleaning steps
	•	Outputs a new cleaned CSV file

Output

cleaned_output.csv



# csv_to_excel.py

A utility script that converts a cleaned CSV file into Excel format.

Features
	•	Prompts for CSV file name
	•	Validates file existence and format
	•	Converts CSV to .xlsx using pandas

Output

cleaned_output.xlsx

# How to Run
	1.	Clean the data:

python clean_data_cli.py

	2.	Convert the cleaned CSV to Excel:

python csv_to_excel.py

# Design Notes
	•	Cleaning and conversion are separated to keep each script focused and reusable
	•	Cleaning behavior is controlled through explicit profiles rather than hard-coded logic
	•	Original input files are never overwritten

# Technologies

Python, pandas, CLI

# Author

Luthando Mbuyane
