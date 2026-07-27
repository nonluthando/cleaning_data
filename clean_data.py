"""CSV data-cleaning tool.

Provides selectable cleaning profiles for preparing datasets
for analysis and machine-learning pipelines.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


PROFILES = {
    "1": {
        "name": "Standard",
        "strip_whitespace": True,
        "drop_duplicates": True,
        "numeric_fill": "median",
        "text_fill": "mode",
        "drop_empty_rows": False,
    },
    "2": {
        "name": "Aggressive",
        "strip_whitespace": True,
        "drop_duplicates": True,
        "numeric_fill": "zero",
        "text_fill": "na",
        "drop_empty_rows": True,
    },
}


def show_profiles() -> None:
    print("Select a cleaning profile:")
    print(
        """
1. Standard
   - Trim whitespace
   - Drop duplicate rows
   - Fill missing numeric values with the median
   - Fill missing text values with the mode or 'N/A'

2. Aggressive
   - Trim whitespace
   - Drop fully empty rows
   - Drop duplicate rows
   - Fill missing numeric values with 0
   - Fill missing text values with 'N/A'
"""
    )


def get_profile(choice: str) -> Optional[Dict[str, Any]]:
    profile = PROFILES.get(choice)

    if profile is None:
        return None

    return profile.copy()


def normalise_text_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Trim text without converting missing values into the string 'nan'."""

    cleaned_dataframe = dataframe.copy()

    text_columns = cleaned_dataframe.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_dataframe[column] = cleaned_dataframe[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

        # Treat blank strings as missing values.
        cleaned_dataframe[column] = cleaned_dataframe[column].replace(
            "",
            pd.NA,
        )

    return cleaned_dataframe


def clean_data(
    dataframe: pd.DataFrame,
    profile: Dict[str, Any],
) -> Tuple[pd.DataFrame, List[str], Dict[str, int]]:

    cleaned_dataframe = dataframe.copy()
    cleaning_log = []

    initial_rows = cleaned_dataframe.shape[0]

    if profile["strip_whitespace"]:
        cleaned_dataframe = normalise_text_columns(cleaned_dataframe)

        cleaning_log.append(
            "Trimmed whitespace and converted blank text values to missing values."
        )

    # Empty rows must be removed before missing values are filled.
    if profile["drop_empty_rows"]:
        rows_before = cleaned_dataframe.shape[0]

        cleaned_dataframe = cleaned_dataframe.dropna(how="all")

        rows_removed = rows_before - cleaned_dataframe.shape[0]

        cleaning_log.append(
            f"Dropped {rows_removed} fully empty rows."
        )

    if profile["drop_duplicates"]:
        rows_before = cleaned_dataframe.shape[0]

        cleaned_dataframe = cleaned_dataframe.drop_duplicates()

        duplicates_removed = (
            rows_before - cleaned_dataframe.shape[0]
        )

        cleaning_log.append(
            f"Dropped {duplicates_removed} duplicate rows."
        )

    numeric_columns = cleaned_dataframe.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        if not cleaned_dataframe[column].isna().any():
            continue

        if profile["numeric_fill"] == "median":
            median_value = cleaned_dataframe[column].median()

            # Use 0 when the entire numeric column is missing.
            if pd.isna(median_value):
                median_value = 0

            cleaned_dataframe[column] = cleaned_dataframe[
                column
            ].fillna(median_value)

            cleaning_log.append(
                f"Filled missing numeric values in "
                f"'{column}' with median ({median_value})."
            )

        else:
            cleaned_dataframe[column] = cleaned_dataframe[
                column
            ].fillna(0)

            cleaning_log.append(
                f"Filled missing numeric values in '{column}' with 0."
            )

    text_columns = cleaned_dataframe.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        if not cleaned_dataframe[column].isna().any():
            continue

        if profile["text_fill"] == "mode":
            mode_values = cleaned_dataframe[column].mode(
                dropna=True
            )

            if mode_values.empty:
                fill_value = "N/A"
            else:
                fill_value = mode_values.iloc[0]

        else:
            fill_value = "N/A"

        cleaned_dataframe[column] = cleaned_dataframe[
            column
        ].fillna(fill_value)

        cleaning_log.append(
            f"Filled missing text values in "
            f"'{column}' with '{fill_value}'."
        )

    cleaned_dataframe = cleaned_dataframe.reset_index(
        drop=True
    )

    final_rows = cleaned_dataframe.shape[0]

    summary = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "rows_removed": initial_rows - final_rows,
    }

    return cleaned_dataframe, cleaning_log, summary


def save_cleaning_log(
    log_path: Path,
    cleaning_log: List[str],
    summary: Dict[str, int],
) -> None:

    lines = [
        "CSV Data Cleaning Log",
        "=====================",
        f"Initial rows: {summary['initial_rows']}",
        f"Final rows: {summary['final_rows']}",
        f"Rows removed: {summary['rows_removed']}",
        "",
        "Cleaning steps:",
    ]

    for entry in cleaning_log:
        lines.append(f"- {entry}")

    log_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    print("=== CSV Data Cleaning Tool ===")

    file_name = input(
        "Please enter the CSV file name: "
    ).strip()

    csv_path = Path(file_name)

    if not csv_path.is_file():
        print("File not found.")
        return

    if csv_path.suffix.lower() != ".csv":
        print("Please provide a CSV file.")
        return

    try:
        dataframe = pd.read_csv(csv_path)

    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")
        return

    except pd.errors.ParserError as error:
        print(f"The CSV file could not be parsed: {error}")
        return

    except OSError as error:
        print(f"The file could not be opened: {error}")
        return

    print("File loaded successfully.")
    print("Initial shape:", dataframe.shape)

    show_profiles()

    choice = input(
        "Enter your choice (1 or 2): "
    ).strip()

    profile = get_profile(choice)

    if profile is None:
        print("Invalid profile selected.")
        return

    print(
        f"Applying {profile['name']} cleaning profile..."
    )

    cleaned_dataframe, cleaning_log, summary = clean_data(
        dataframe,
        profile,
    )

    output_path = csv_path.with_name(
        f"{csv_path.stem}_cleaned.csv"
    )

    log_path = csv_path.with_name(
        f"{csv_path.stem}_cleaning_log.txt"
    )

    try:
        cleaned_dataframe.to_csv(
            output_path,
            index=False,
        )

        save_cleaning_log(
            log_path,
            cleaning_log,
            summary,
        )

    except OSError as error:
        print(f"Could not save the output files: {error}")
        return

    print(
        f"Initial number of rows: "
        f"{summary['initial_rows']}"
    )

    print(
        f"Final number of rows: "
        f"{summary['final_rows']}"
    )

    print(
        f"Number of rows removed: "
        f"{summary['rows_removed']}"
    )

    print("\n--- Cleaning Log ---")

    for entry in cleaning_log:
        print("-", entry)

    print("\nCleaned file saved as:", output_path)
    print("Cleaning log saved as:", log_path)

    print("\n--- Sample of Cleaned Data ---")
    print(cleaned_dataframe.head())


if __name__ == "__main__":
    main()
