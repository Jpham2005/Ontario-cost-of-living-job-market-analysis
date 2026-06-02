import pandas as pd
import matplotlib.pyplot as plt
import os

CPI_FILE = "data/cleaned/cleaned_cpi_ontario.csv"
LABOUR_FILE = "data/cleaned/cleaned_labour_ontario.csv"

CHARTS_FOLDER = "charts"


def create_cpi_trend_chart():
    df = pd.read_csv(CPI_FILE)
    df["Date"] = pd.to_datetime(df["Date"])

    # Keep project range
    df = df[(df["Year"] >= 2019) & (df["Year"] <= 2025)]

    plt.figure(figsize=(12, 6))

    for category in df["Category"].unique():
        category_data = df[df["Category"] == category]
        plt.plot(category_data["Date"], category_data["CPI_Value"], label=category)

    plt.title("Ontario CPI Trend by Category (2019-2025)")
    plt.xlabel("Year")
    plt.ylabel("CPI Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"{CHARTS_FOLDER}/ontario_cpi_trend.png")
    plt.close()


def create_yearly_cpi_chart():
    df = pd.read_csv(CPI_FILE)

    df = df[(df["Year"] >= 2019) & (df["Year"] <= 2025)]

    yearly_cpi = df.groupby(["Year", "Category"])["CPI_Value"].mean().reset_index()

    pivot_df = yearly_cpi.pivot(index="Year", columns="Category", values="CPI_Value")

    pivot_df.plot(kind="bar", figsize=(12, 6))

    plt.title("Average Yearly CPI by Category in Ontario")
    plt.xlabel("Year")
    plt.ylabel("Average CPI Value")
    plt.xticks(rotation=45)
    plt.legend(title="Category")
    plt.tight_layout()

    plt.savefig(f"{CHARTS_FOLDER}/yearly_cpi_comparison.png")
    plt.close()


def create_unemployment_rate_chart():
    df = pd.read_csv(LABOUR_FILE)
    df["Date"] = pd.to_datetime(df["Date"])

    df = df[(df["Year"] >= 2019) & (df["Year"] <= 2025)]

    unemployment_rate = df[df["Indicator"] == "Unemployment rate"]

    plt.figure(figsize=(12, 6))
    plt.plot(unemployment_rate["Date"], unemployment_rate["Value"])

    plt.title("Ontario Unemployment Rate Trend (2019-2025)")
    plt.xlabel("Year")
    plt.ylabel("Unemployment Rate (%)")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"{CHARTS_FOLDER}/unemployment_rate_trend.png")
    plt.close()


def create_employment_chart():
    df = pd.read_csv(LABOUR_FILE)
    df["Date"] = pd.to_datetime(df["Date"])

    df = df[(df["Year"] >= 2019) & (df["Year"] <= 2025)]

    employment_data = df[df["Indicator"].isin(["Employment", "Unemployment"])]

    plt.figure(figsize=(12, 6))

    for indicator in employment_data["Indicator"].unique():
        indicator_data = employment_data[employment_data["Indicator"] == indicator]
        plt.plot(indicator_data["Date"], indicator_data["Value"], label=indicator)

    plt.title("Ontario Employment and Unemployment Trend (2019-2025)")
    plt.xlabel("Year")
    plt.ylabel("Persons in Thousands")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"{CHARTS_FOLDER}/employment_unemployment_trend.png")
    plt.close()


def main():
    os.makedirs(CHARTS_FOLDER, exist_ok=True)

    create_cpi_trend_chart()
    create_yearly_cpi_chart()
    create_unemployment_rate_chart()
    create_employment_chart()

    print("Charts created successfully.")


if __name__ == "__main__":
    main()