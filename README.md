# CSV Data Cleaning and Excel Conversion Utility

## Overview

This utility was created to speed up repetitive data-preparation tasks while working on the analysis projects in my data analyst portfolio.

Many datasets sourced from platforms such as Kaggle are provided as CSV files. While Python and pandas are useful for cleaning and analysing these datasets, I sometimes wanted to continue the analysis in Excel using tools such as PivotTables, charts and spreadsheet-based exploration.

Instead of manually cleaning and converting each dataset, I created reusable Python scripts that:

- Clean common data-quality issues
- Produce an analysis-ready CSV file
- Record the cleaning operations applied
- Convert the cleaned CSV into Excel format

This allowed me to move more quickly from raw data to analysis.

## Workflow

```text
Kaggle or other CSV dataset
            ↓
Python cleaning script
            ↓
Cleaned CSV + cleaning log
            ↓
CSV-to-Excel conversion
            ↓
Analysis in Python, Excel or both
```

## Why I Built It

During my data-analysis projects, I repeatedly encountered similar preparation tasks:

- Removing duplicate records
- Handling missing values
- Trimming inconsistent whitespace
- Cleaning blank text fields
- Converting CSV datasets into Excel workbooks
- Preparing data for PivotTables and reporting

Automating these steps reduced repeated manual work and made the preparation process more consistent across projects.

The utility supports the larger projects available in my data analyst portfolio rather than functioning as a separate analysis project.

## Features

- Selectable standard and aggressive cleaning profiles
- Duplicate-row removal
- Whitespace and blank-value normalisation
- Missing numeric-value handling
- Missing text-value handling
- Optional removal of fully empty rows
- Cleaning summaries and transformation logs
- CSV-to-Excel conversion
- Input-file validation and error handling

## Project Files

### `clean_data.py`

An interactive Python command-line script that:

- Loads and validates a CSV file
- Applies the selected cleaning profile
- Cleans missing and inconsistent values
- Removes duplicate records
- Produces a cleaned CSV
- Creates a text log of the transformations applied

### `csv_to_excel.py`

Converts a cleaned CSV file into an Excel workbook for further analysis, PivotTable creation, charting and sharing.

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

Install the required packages:

```bash
pip install pandas openpyxl
```

## How to Use

### 1. Download the Repository

```bash
git clone https://github.com/nonluthando/cleaning_data.git
cd cleaning_data
```

You can also download the repository as a ZIP file from GitHub.

### 2. Add the Dataset

Place the CSV file in the same folder as the scripts.

Example:

```text
cleaning_data/
├── clean_data.py
├── csv_to_excel.py
└── customer_data.csv
```

### 3. Clean the Dataset

Run:

```bash
python clean_data.py
```

Enter the filename when prompted:

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

The script creates:

```text
customer_data_cleaned.csv
customer_data_cleaning_log.txt
```

### 4. Convert the Cleaned Dataset to Excel

Run:

```bash
python csv_to_excel.py
```

Enter:

```text
customer_data_cleaned.csv
```

The script creates:

```text
customer_data_cleaned.xlsx
```

The Excel file can then be used for:

- PivotTables
- Charts
- Spreadsheet exploration
- Reporting
- Sharing analysis outputs

## Using Google Colab

Upload the following files to Google Colab:

- `clean_data.py`
- `csv_to_excel.py`
- The CSV dataset

Install the dependencies:

```python
!pip install pandas openpyxl
```

Run the cleaning script:

```python
%run clean_data.py
```

Run the Excel converter:

```python
%run csv_to_excel.py
```

The generated files can be downloaded from the Colab Files panel.

## Portfolio Context

This utility supports the end-to-end analysis projects in my data analyst portfolio.

It demonstrates how I used Python to improve my own analytical workflow by automating repetitive preparation tasks and making it easier to work across both Python and Excel.

## Technologies

- Python
- pandas
- openpyxl
- CSV
- Microsoft Excel
