import pandas as pd

cpi_file = "data/raw/cpi_ontario.csv"
labour_file = "data/raw/labour_ontario.csv"


def find_header_row(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        cleaned_line = line.strip().replace('"', "")

        # Real Statistics Canada CSV header usually starts like this
        if cleaned_line.startswith("REF_DATE,") or cleaned_line.startswith("REF_DATE;"):
            return index

    raise ValueError(f"Could not find real header row in {file_path}")


def read_statcan_csv(file_path):
    header_row = find_header_row(file_path)
    print(f"Header row found at line: {header_row + 1}")

    return pd.read_csv(
        file_path,
        skiprows=header_row,
        encoding="utf-8-sig",
        engine="python",
        on_bad_lines="skip"
    )


print("Checking CPI file...")
cpi_df = read_statcan_csv(cpi_file)
print(cpi_df.head())
print(cpi_df.columns)

print("\nChecking Labour file...")
labour_df = read_statcan_csv(labour_file)
print(labour_df.head())
print(labour_df.columns)

print("\nBoth files loaded successfully.")