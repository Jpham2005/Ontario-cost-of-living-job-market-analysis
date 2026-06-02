import pandas as pd
import os

CPI_RAW_FILE = "data/raw/cpi_ontario.csv"
LABOUR_RAW_FILE = "data/raw/labour_ontario.csv"

CPI_CLEAN_FILE = "data/cleaned/cleaned_cpi_ontario.csv"
LABOUR_CLEAN_FILE = "data/cleaned/cleaned_labour_ontario.csv"


def clean_number(value):
    if pd.isna(value):
        return None

    value = str(value).replace(",", "").strip()

    try:
        return float(value)
    except ValueError:
        return None


def clean_cpi_data():
    print("Cleaning CPI data...")

    df = pd.read_csv(CPI_RAW_FILE, encoding="utf-8-sig")

    print("CPI columns:")
    print(df.columns)

    # Keep Ontario only
    df = df[df["GEO"].astype(str).str.contains("Ontario", case=False, na=False)]

    # Clean category names because StatCan sometimes adds spaces or numbers
    df["Category"] = (
        df["Products and product groups"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+\d+$", "", regex=True)
    )

    print("CPI categories found:")
    print(df["Category"].drop_duplicates())

    categories = [
        "All-items",
        "Food",
        "Shelter",
        "Transportation",
        "Energy"
    ]

    df = df[df["Category"].isin(categories)]

    df["Date"] = pd.to_datetime(df["REF_DATE"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    df["CPI_Value"] = df["VALUE"].apply(clean_number)

    df = df[[
        "Date",
        "Year",
        "Month",
        "GEO",
        "Category",
        "CPI_Value"
    ]]

    df = df.rename(columns={
        "GEO": "Province"
    })

    df = df.dropna()
    df = df.drop_duplicates()

    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(CPI_CLEAN_FILE, index=False)

    print("Cleaned CPI data saved.")
    print(df.head())


def clean_labour_data():
    print("\nCleaning labour data...")

    df = pd.read_csv(LABOUR_RAW_FILE, encoding="utf-8-sig")

    print("Labour columns:")
    print(df.columns)

    df = df[df["GEO"].astype(str).str.contains("Ontario", case=False, na=False)]

    indicators = [
        "Employment",
        "Unemployment",
        "Unemployment rate"
    ]

    df = df[df["Labour force characteristics"].isin(indicators)]

    if "Data type" in df.columns:
        df = df[df["Data type"].str.contains("Seasonally adjusted", na=False)]

    df["Date"] = pd.to_datetime(df["REF_DATE"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    df["Value"] = df["VALUE"].apply(clean_number)

    df = df[[
        "Date",
        "Year",
        "Month",
        "GEO",
        "Labour force characteristics",
        "Value"
    ]]

    df = df.rename(columns={
        "GEO": "Province",
        "Labour force characteristics": "Indicator"
    })

    df = df.dropna()
    df = df.drop_duplicates()

    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(LABOUR_CLEAN_FILE, index=False)

    print("Cleaned labour data saved.")
    print(df.head())


if __name__ == "__main__":
    clean_cpi_data()
    clean_labour_data()
    print("\nAll cleaning finished successfully.")