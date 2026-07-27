# Data Cleaning and Format Conversion Utility

## Overview

This utility was created to speed up repetitive data-preparation tasks while working on projects in my data analyst portfolio, including customer churn and product drop-off analysis.

Many datasets sourced from platforms such as Kaggle are provided as CSV files. I often cleaned and explored the data using Python, but sometimes wanted to continue the analysis in Excel using PivotTables, charts and spreadsheet-based exploration.

Instead of manually cleaning and converting each dataset, I created reusable Python scripts that:

- Clean common data-quality issues
- Produce analysis-ready datasets
- Record the cleaning operations applied
- Convert data between CSV, Excel and Parquet formats

This utility supports my larger analysis projects rather than functioning as a standalone analysis project.

## Workflow

```text
Kaggle or other raw dataset
            ↓
Data cleaning with Python
            ↓
Cleaned dataset + cleaning log
            ↓
Format conversion when required
            ↓
Analysis in Python, Excel or both
```

## Why I Built It

While working on data-analysis projects, I repeatedly encountered similar preparation tasks:

- Removing duplicate records
- Handling missing values
- Trimming inconsistent whitespace
- Cleaning blank text fields
- Converting CSV datasets into Excel workbooks
- Preparing data for PivotTables and charts
- Converting datasets into Parquet for more efficient storage and processing

Automating these steps reduced repeated manual work and made my preparation process more consistent across projects.

## Features

### Data Cleaning

- Standard and aggressive cleaning profiles
- Duplicate-row removal
- Whitespace normalisation
- Blank-string handling
- Missing numeric-value handling
- Missing text-value handling
- Optional removal of fully empty rows
- Cleaning summaries
- Transformation logs
- Input-file validation and error handling

### Data Conversion

- CSV to Excel
- CSV to Parquet
- Excel to CSV
- Excel to Parquet
- Parquet to CSV
- Parquet to Excel
- Automatic input-format detection
- Excel worksheet selection
- Multi-sheet Excel export
- Automatic output naming
- Custom output paths
- Overwrite protection

## Project Files

### `clean_data.py`

An interactive command-line tool that:

- Loads and validates a CSV file
- Applies a selected cleaning profile
- Handles missing and inconsistent values
- Removes duplicate records
- Produces a cleaned CSV file
- Creates a text log describing the transformations applied

### `convert_data.py`

A command-line conversion tool that converts tabular datasets between:

- CSV
- Excel
- Parquet

Runtime parameters determine the required output format, worksheet and output location.

## Cleaning Profiles

### Standard Profile

The standard profile:

- Trims whitespace in text columns
- Converts blank strings into missing values
- Removes duplicate rows
- Fills missing numeric values using the column median
- Fills missing text values using the column mode
- Uses `N/A` when no text mode is available

### Aggressive Profile

The aggressive profile:

- Trims whitespace in text columns
- Converts blank strings into missing values
- Removes fully empty rows
- Removes duplicate rows
- Fills missing numeric values with `0`
- Fills missing text values with `N/A`

## Requirements

- Python 3
- pandas
- openpyxl
- pyarrow

Install the required packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
pandas
openpyxl
pyarrow
```

## How to Use

### 1. Download the Repository

Clone the repository:

```bash
git clone https://github.com/nonluthando/cleaning_data.git
cd cleaning_data
```

You can also download the repository as a ZIP file from GitHub.

### 2. Add a Dataset

Place the dataset in the same folder as the scripts.

Example:

```text
cleaning_data/
├── clean_data.py
├── convert_data.py
├── requirements.txt
└── customer_data.csv
```

## Cleaning a CSV Dataset

Run:

```bash
python clean_data.py
```

Enter the CSV filename when prompted:

```text
customer_data.csv
```

Choose a cleaning profile:

```text
1
```

for the Standard profile, or:

```text
2
```

for the Aggressive profile.

For a file named `customer_data.csv`, the script creates:

```text
customer_data_cleaned.csv
customer_data_cleaning_log.txt
```

The log records:

- Initial row count
- Final row count
- Number of rows removed
- Cleaning operations applied
- Missing-value replacements
- Duplicate and empty-row removals

## Converting Data Formats

The conversion command follows this structure:

```bash
python convert_data.py INPUT_FILE --to OUTPUT_FORMAT
```

Supported output formats are:

```text
csv
xlsx
parquet
```

### CSV to Excel

```bash
python convert_data.py customer_data.csv --to xlsx
```

Output:

```text
customer_data.xlsx
```

### CSV to Parquet

```bash
python convert_data.py customer_data.csv --to parquet
```

Output:

```text
customer_data.parquet
```

### Excel to CSV

```bash
python convert_data.py customer_data.xlsx --to csv
```

### Excel to Parquet

```bash
python convert_data.py customer_data.xlsx --to parquet
```

### Parquet to CSV

```bash
python convert_data.py customer_data.parquet --to csv
```

### Parquet to Excel

```bash
python convert_data.py customer_data.parquet --to xlsx
```

## Excel Worksheet Selection

When an Excel workbook contains multiple worksheets, specify the sheet to convert:

```bash
python convert_data.py report.xlsx --to csv --sheet "Customer Data"
```

The same option can be used when converting Excel to Parquet:

```bash
python convert_data.py report.xlsx --to parquet --sheet "Customer Data"
```

## Converting All Excel Worksheets

Convert every worksheet into a separate CSV file:

```bash
python convert_data.py report.xlsx --to csv --all-sheets
```

Convert every worksheet into a separate Parquet file:

```bash
python convert_data.py report.xlsx --to parquet --all-sheets
```

The files are placed in an automatically generated output folder.

Example:

```text
report_csv_sheets/
├── report_01_Customers.csv
├── report_02_Products.csv
└── report_03_Orders.csv
```

## Custom Output Filename

Specify the output filename using `--output`:

```bash
python convert_data.py customer_data.csv \
  --to xlsx \
  --output prepared_customer_data.xlsx
```

For `--all-sheets`, the output value must be a directory:

```bash
python convert_data.py report.xlsx \
  --to csv \
  --all-sheets \
  --output exported_sheets
```

## Overwriting Existing Files

The converter does not replace existing files by default.

Use `--overwrite` when you intentionally want to replace an output file:

```bash
python convert_data.py customer_data.csv \
  --to xlsx \
  --overwrite
```

## Using Google Colab

Upload the following files to Google Colab:

- `clean_data.py`
- `convert_data.py`
- The dataset you want to process

Install the dependencies:

```python
!pip install pandas openpyxl pyarrow
```

Run the cleaning script:

```python
%run clean_data.py
```

Run the conversion script:

```python
!python convert_data.py customer_data_cleaned.csv --to xlsx
```

Example Parquet conversion:

```python
!python convert_data.py customer_data_cleaned.csv --to parquet
```

The generated files can be downloaded from the Colab Files panel.

## Important Format Limitations

CSV files store plain tabular data only.

When converting Excel to CSV or Parquet, the following Excel features are not preserved:

- PivotTables
- Charts
- Formatting
- Formulas
- Macros
- Multiple worksheets in one output file

When using `--all-sheets`, each worksheet is exported as a separate file.

Parquet generally preserves column data types more reliably than CSV and is more suitable for larger analytical datasets.

## Portfolio Context

This utility supports projects in my data analyst portfolio, including customer churn and product drop-off analysis.

It demonstrates how I used Python to improve my own analytical workflow by automating repetitive data preparation and making it easier to move between Python, Excel and efficient analytical storage formats.

## Technologies

- Python
- pandas
- openpyxl
- pyarrow
- CSV
- Microsoft Excel
- Apache Parquet
