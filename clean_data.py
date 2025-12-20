import pandas as pd
import os

def show_profiles():
    print("Select a cleaning profile:")
    print("""
    1. Standard (safe cleaning)
       - Trim whitespace in text columns
       - Drop duplicate rows
       - Fill missing numeric values with median
       - Fill missing text values with mode or 'N/A'

    2. Aggressive (heavy cleaning)
       - Trim whitespace in text columns
       - Drop duplicate rows
       - Fill missing numeric values with 0
       - Fill missing text values with 'N/A'
       - Drop fully empty rows
    """)

def get_profile(choice):
    if choice == "1":
        return {
            "name": "Standard",
            "strip_whitespace": True,
            "drop_duplicates": True,
            "numeric_fill": "median",
            "text_fill": "mode",
            "drop_empty_rows": False
        }
    elif choice == "2":
        return {
            "name": "Aggressive",
            "strip_whitespace": True,
            "drop_duplicates": True,
            "numeric_fill": "zero",
            "text_fill": "na",
            "drop_empty_rows": True
        }
    else:
        return None

def clean_data(df, profile):
    log = []
    initial_rows = df.shape[0]

    if profile["strip_whitespace"]:
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()
        log.append("Trimmed whitespace in text columns.")

    if profile["drop_duplicates"]:
        before = df.shape[0]
        df = df.drop_duplicates()
        log.append(f"Dropped {before - df.shape[0]} duplicate rows.")

    for col in df.select_dtypes(include="number").columns:
        if df[col].isna().any():
            if profile["numeric_fill"] == "median":
                value = df[col].median()
                df[col] = df[col].fillna(value)
                log.append(f"Filled missing numeric values in '{col}' with median ({value}).")
            else:
                df[col] = df[col].fillna(0)
                log.append(f"Filled missing numeric values in '{col}' with 0.")

    for col in df.select_dtypes(include="object").columns:
        if df[col].isna().any():
            if profile["text_fill"] == "mode":
                mode_vals = df[col].mode()
                fill_value = mode_vals[0] if not mode_vals.empty else "N/A"
                df[col] = df[col].fillna(fill_value)
                log.append(f"Filled missing text values in '{col}' with '{fill_value}'.")
            else:
                df[col] = df[col].fillna("N/A")
                log.append(f"Filled missing text values in '{col}' with 'N/A'.")

    if profile["drop_empty_rows"]:
        before = df.shape[0]
        df = df.dropna(how="all")
        log.append(f"Dropped {before - df.shape[0]} fully empty rows.")

    final_rows = df.shape[0]

    summary = {
        "initial_rows": initial_rows,
        "final_rows": final_rows,
        "rows_removed": initial_rows - final_rows
    }

    return df, log, summary

def main():
    print("=== CSV Data Cleaning Tool ===")

    file_name = input("Please enter the CSV file name: ").strip()

    if not os.path.exists(file_name):
        print("File not found.")
        return

    df = pd.read_csv(file_name)
    print("File loaded successfully.")
    print("Initial shape:", df.shape)

    show_profiles()
    choice = input("Enter your choice (1 or 2): ").strip()
    profile = get_profile(choice)

    if not profile:
        print("Invalid profile selected.")
        return

    print(f"Applying {profile['name']} cleaning profile...")

    cleaned_df, log, summary = clean_data(df, profile)

    print(f"Initial number of rows: {summary['initial_rows']}")
    print(f"Final number of rows: {summary['final_rows']}")
    print(f"Number of rows removed: {summary['rows_removed']}")

    print("\n--- Cleaning Log ---")
    for entry in log:
        print("-", entry)

    output_file = "cleaned_output.csv"
    cleaned_df.to_csv(output_file, index=False)

    print("\nCleaned file saved as:", output_file)
    print("\n--- Sample of Cleaned Data ---")
    print(cleaned_df.head())

if __name__ == "__main__":
    main()
