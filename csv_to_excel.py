import pandas as pd
from pathlib import Path

def main():
    print("=== Cleaned CSV to Excel Converter ===")

    file_name = input("Please enter the cleaned CSV file name: ").strip()
    csv_path = Path(file_name)

    if not csv_path.exists():
        print("File not found.")
        return

    if csv_path.suffix.lower() != ".csv":
        print("Please provide a CSV file.")
        return

    # Read cleaned CSV
    df = pd.read_csv(csv_path)
    print("File loaded successfully.")
    print("Shape:", df.shape)

    # Generate Excel output filename
    output_file = csv_path.with_suffix(".xlsx")

    # Export to Excel
    df.to_excel(output_file, index=False)

    print(f"Excel file created: {output_file}")

if __name__ == "__main__":
    main()
