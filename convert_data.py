"""Convert tabular data between CSV, Excel and Parquet formats."""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

import pandas as pd


SUPPORTED_INPUT_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".parquet",
}

TARGET_EXTENSIONS = {
    "csv": ".csv",
    "xlsx": ".xlsx",
    "parquet": ".parquet",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert files between CSV, Excel and Parquet formats."
        )
    )

    parser.add_argument(
        "input_file",
        help="Path to the CSV, Excel or Parquet file.",
    )

    parser.add_argument(
        "--to",
        required=True,
        choices=["csv", "xlsx", "parquet"],
        help="Output format.",
    )

    excel_options = parser.add_mutually_exclusive_group()

    excel_options.add_argument(
        "--sheet",
        help="Excel worksheet to convert.",
    )

    excel_options.add_argument(
        "--all-sheets",
        action="store_true",
        help="Convert every Excel worksheet into a separate file.",
    )

    parser.add_argument(
        "--output",
        help=(
            "Custom output file. When using --all-sheets, "
            "this must be an output directory."
        ),
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow existing output files to be replaced.",
    )

    return parser


def get_source_format(input_path: Path) -> str:
    extension = input_path.suffix.lower()

    if extension not in SUPPORTED_INPUT_EXTENSIONS:
        supported = ", ".join(
            sorted(SUPPORTED_INPUT_EXTENSIONS)
        )

        raise ValueError(
            f"Unsupported input format '{extension}'. "
            f"Supported formats: {supported}"
        )

    return extension.removeprefix(".")


def validate_arguments(
    input_path: Path,
    source_format: str,
    target_format: str,
    sheet: Optional[str],
    all_sheets: bool,
) -> None:
    if not input_path.is_file():
        raise ValueError(
            f"Input file not found: {input_path}"
        )

    if source_format != "xlsx" and sheet is not None:
        raise ValueError(
            "--sheet can only be used with Excel files."
        )

    if source_format != "xlsx" and all_sheets:
        raise ValueError(
            "--all-sheets can only be used with Excel files."
        )

    if all_sheets and target_format == "xlsx":
        raise ValueError(
            "Converting every Excel sheet into separate Excel files "
            "is not supported because the source is already Excel."
        )

    if (
        source_format == target_format
        and not all_sheets
    ):
        raise ValueError(
            f"The input is already in {target_format.upper()} format."
        )


def normalise_output_path(
    output_value: Optional[str],
    input_path: Path,
    target_format: str,
) -> Path:
    expected_extension = TARGET_EXTENSIONS[target_format]

    if output_value is None:
        return input_path.with_suffix(expected_extension)

    output_path = Path(output_value)

    if output_path.suffix == "":
        return output_path.with_suffix(expected_extension)

    if output_path.suffix.lower() != expected_extension:
        raise ValueError(
            f"The output filename must end with "
            f"'{expected_extension}'."
        )

    return output_path


def ensure_output_available(
    output_path: Path,
    overwrite: bool,
) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output already exists: {output_path}\n"
            "Use --overwrite to replace it."
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def read_standard_file(
    input_path: Path,
    source_format: str,
) -> pd.DataFrame:
    if source_format == "csv":
        return pd.read_csv(input_path)

    if source_format == "parquet":
        return pd.read_parquet(input_path)

    raise ValueError(
        f"Unsupported standard input format: {source_format}"
    )


def get_excel_sheet_names(
    input_path: Path,
) -> List[str]:
    with pd.ExcelFile(input_path) as workbook:
        return workbook.sheet_names


def choose_excel_sheet(
    input_path: Path,
    requested_sheet: Optional[str],
) -> str:
    sheet_names = get_excel_sheet_names(input_path)

    if not sheet_names:
        raise ValueError(
            "The Excel workbook does not contain any worksheets."
        )

    if requested_sheet is not None:
        if requested_sheet not in sheet_names:
            available_sheets = ", ".join(sheet_names)

            raise ValueError(
                f"Worksheet '{requested_sheet}' was not found.\n"
                f"Available worksheets: {available_sheets}"
            )

        return requested_sheet

    if len(sheet_names) > 1:
        available_sheets = ", ".join(sheet_names)

        raise ValueError(
            "The workbook contains multiple worksheets.\n"
            f"Available worksheets: {available_sheets}\n"
            "Use --sheet followed by a worksheet name, "
            "or use --all-sheets."
        )

    return sheet_names[0]


def read_excel_sheet(
    input_path: Path,
    sheet_name: str,
) -> pd.DataFrame:
    return pd.read_excel(
        input_path,
        sheet_name=sheet_name,
    )


def write_dataframe(
    dataframe: pd.DataFrame,
    output_path: Path,
    target_format: str,
    overwrite: bool,
    worksheet_name: str = "Data",
) -> None:
    ensure_output_available(
        output_path,
        overwrite,
    )

    if target_format == "csv":
        dataframe.to_csv(
            output_path,
            index=False,
        )

    elif target_format == "xlsx":
        dataframe.to_excel(
            output_path,
            index=False,
            sheet_name=worksheet_name[:31],
        )

    elif target_format == "parquet":
        dataframe.to_parquet(
            output_path,
            index=False,
        )

    else:
        raise ValueError(
            f"Unsupported output format: {target_format}"
        )


def sanitise_filename(value: str) -> str:
    cleaned_value = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        value,
    )

    cleaned_value = re.sub(
        r"\s+",
        "_",
        cleaned_value.strip(),
    )

    return cleaned_value or "sheet"


def convert_single_file(
    input_path: Path,
    source_format: str,
    target_format: str,
    output_value: Optional[str],
    requested_sheet: Optional[str],
    overwrite: bool,
) -> Path:
    worksheet_name = "Data"

    if source_format == "xlsx":
        worksheet_name = choose_excel_sheet(
            input_path,
            requested_sheet,
        )

        dataframe = read_excel_sheet(
            input_path,
            worksheet_name,
        )

    else:
        dataframe = read_standard_file(
            input_path,
            source_format,
        )

    output_path = normalise_output_path(
        output_value,
        input_path,
        target_format,
    )

    write_dataframe(
        dataframe=dataframe,
        output_path=output_path,
        target_format=target_format,
        overwrite=overwrite,
        worksheet_name=worksheet_name,
    )

    return output_path


def convert_all_excel_sheets(
    input_path: Path,
    target_format: str,
    output_value: Optional[str],
    overwrite: bool,
) -> List[Path]:
    sheet_names = get_excel_sheet_names(input_path)

    if not sheet_names:
        raise ValueError(
            "The Excel workbook does not contain any worksheets."
        )

    if output_value is None:
        output_directory = input_path.parent / (
            f"{input_path.stem}_{target_format}_sheets"
        )
    else:
        output_directory = Path(output_value)

        if output_directory.suffix:
            raise ValueError(
                "When using --all-sheets, --output must be "
                "a directory rather than a filename."
            )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = TARGET_EXTENSIONS[target_format]
    output_paths = []

    for position, sheet_name in enumerate(
        sheet_names,
        start=1,
    ):
        dataframe = read_excel_sheet(
            input_path,
            sheet_name,
        )

        safe_sheet_name = sanitise_filename(
            sheet_name
        )

        output_filename = (
            f"{input_path.stem}_"
            f"{position:02d}_"
            f"{safe_sheet_name}"
            f"{extension}"
        )

        output_path = (
            output_directory / output_filename
        )

        write_dataframe(
            dataframe=dataframe,
            output_path=output_path,
            target_format=target_format,
            overwrite=overwrite,
            worksheet_name=sheet_name,
        )

        output_paths.append(output_path)

    return output_paths


def main() -> None:
    parser = build_parser()
    arguments = parser.parse_args()

    input_path = Path(arguments.input_file)

    try:
        source_format = get_source_format(
            input_path
        )

        validate_arguments(
            input_path=input_path,
            source_format=source_format,
            target_format=arguments.to,
            sheet=arguments.sheet,
            all_sheets=arguments.all_sheets,
        )

        if arguments.all_sheets:
            output_paths = convert_all_excel_sheets(
                input_path=input_path,
                target_format=arguments.to,
                output_value=arguments.output,
                overwrite=arguments.overwrite,
            )

            print(
                f"Converted {len(output_paths)} worksheets:"
            )

            for output_path in output_paths:
                print(f"- {output_path}")

        else:
            output_path = convert_single_file(
                input_path=input_path,
                source_format=source_format,
                target_format=arguments.to,
                output_value=arguments.output,
                requested_sheet=arguments.sheet,
                overwrite=arguments.overwrite,
            )

            print(
                f"Conversion completed: {output_path}"
            )

    except (
        ValueError,
        FileExistsError,
        OSError,
        ImportError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ) as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
