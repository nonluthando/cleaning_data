# CSV Data Cleaning & Conversion Pipeline

## Overview

This project provides a Python-based data-preparation pipeline for converting raw CSV datasets into clean, analysis-ready CSV and Excel files.

It handles common data-quality issues such as:

- Missing values
- Duplicate rows
- Extra whitespace
- Blank text values
- Fully empty rows
- Inconsistent file formats

The pipeline reduces repetitive manual data preparation and records the transformations applied for greater traceability.

## Pipeline Flow

```text
Raw CSV
   ↓
Data Cleaning and Validation
   ↓
Cleaned CSV + Cleaning Log
   ↓
CSV-to-Excel Conversion
   ↓
Analysis-Ready Excel File
```

## Key Features

- Two selectable cleaning profiles
- Safe handling of missing values
- Whitespace and blank-value normalisation
- Duplicate-row removal
- Median-based numeric imputation
- Mode-based text imputation
- Cleaning summaries and transformation logs
- CSV-to-Excel conversion
- Input-file validation and error handling
- Support for local Python environments and Google Colab

## Project Files

### `clean_data.py`

Interactive command-line tool that:

- Loads and validates a CSV file
- Applies a selected cleaning profile
- Cleans missing and inconsistent values
- Removes duplicates
- Produces a cleaned CSV file
- Creates a text log describing the transformations

### `csv_to_excel.py`

Converts a cleaned CSV file into Excel format for analysis, reporting and sharing.

## Cleaning Profiles

### 1. Standard Profile

The standard profile performs safer cleaning:

- Trims whitespace in text columns
- Converts blank strings into missing values
- Removes duplicate rows
- Fills missing numeric values with the column median
- Fills missing text values with the column mode
- Uses `N/A` when no text mode is available

### 2. Aggressive Profile

The aggressive profile performs heavier cleaning:

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

Install the required packages:

```bash
pip install pandas openpyxl
```

## How to Use

### 1. Download the Project

Clone the repository:

```bash
git clone https://github.com/nonluthando/cleaning_data.git
cd cleaning_data
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### 2. Add a CSV File

Place the CSV file you want to clean in the project folder.

Example:

```text
cleaning_data/
├── clean_data.py
├── csv_to_excel.py
└── customers.csv
```

### 3. Run the Cleaning Tool

Run:

```bash
python clean_data.py
```

When prompted, enter the CSV filename:

```text
customers.csv
```

Then select a cleaning profile:

```text
1
```

for the Standard profile, or:

```text
2
```

for the Aggressive profile.

### 4. Review the Outputs

For a file named `customers.csv`, the cleaning tool creates:

```text
customers_cleaned.csv
customers_cleaning_log.txt
```

The cleaned CSV contains the processed data.

The cleaning log records:

- Initial row count
- Final row count
- Number of rows removed
- Cleaning operations applied
- Missing-value replacements
- Duplicate and empty-row removals

### 5. Convert the Cleaned CSV to Excel

Run:

```bash
python csv_to_excel.py
```

When prompted, enter:

```text
customers_cleaned.csv
```

The converter creates:

```text
customers_cleaned.xlsx
```

## Using Google Colab

Upload the following files to a Google Colab notebook:

- `clean_data.py`
- `csv_to_excel.py`
- The CSV file you want to clean

Install the dependencies:

```python
!pip install pandas openpyxl
```

Run the cleaning tool:

```python
%run clean_data.py
```

Enter the uploaded CSV filename when prompted.

Then run the Excel converter:

```python
%run csv_to_excel.py
```

The generated CSV, log and Excel files can be downloaded from the Colab Files panel.

## Example

Input file:

```text
employee_data.csv
```

After running the cleaning tool:

```text
employee_data_cleaned.csv
employee_data_cleaning_log.txt
```

After running the Excel converter:

```text
employee_data_cleaned.xlsx
```

## Intended Use

This pipeline is designed for situations where analysts, researchers or developers regularly receive raw or inconsistently formatted CSV files.

It provides a repeatable preprocessing step before:

- Exploratory data analysis
- Statistical analysis
- Dashboard development
- Reporting
- Machine-learning workflows
- Database imports
- Business decision-support processes

## Technologies

- Python
- pandas
- openpyxl
- CSV
- Microsoft Excel
