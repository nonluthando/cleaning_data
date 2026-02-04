# CSV Data Cleaning & Conversion Pipeline

## Overview

This project implements a modular data-preparation pipeline designed to convert raw CSV datasets into clean, analysis-ready Excel files. It focuses on improving data quality, consistency, and reproducibility prior to analysis, addressing common issues such as missing values, inconsistent formatting, and invalid records.

The pipeline is intended to support analysts by reducing manual data preparation time and ensuring that downstream analysis is based on reliable inputs.

## Problem Context

Raw datasets often require significant cleaning before analysis can begin. Inconsistent schemas, missing values, and formatting errors introduce risk and slow down analytical workflows. This project formalises the data-cleaning step into a repeatable process, improving reliability and transparency.

## Pipeline Flow

Raw CSV
→ Data Cleaning & Validation (CLI-driven)
→ Cleaned CSV
→ CSV-to-Excel Conversion
→ Analysis-Ready Excel File


## Key Features
	•	Modular cleaning stages to support different dataset structures
	•	Configurable cleaning profiles for flexible handling of missing values and inconsistencies
	•	Validation and logging to improve traceability and reproducibility
	•	Excel output to support common analyst and stakeholder workflows

## Scripts

clean_data.py
Interactive command-line tool for cleaning CSV datasets using configurable cleaning profiles. Supports validation, standardisation, and preparation for downstream analysis.

convert_to_excel.py

Converts cleaned CSV outputs into Excel format for ease of analysis and sharing.

## Intended Use
This pipeline is designed as a supporting tool for analytical work, particularly in scenarios where analysts regularly receive raw or inconsistently formatted data and need a reliable preprocessing step before exploration, reporting, or modelling.
