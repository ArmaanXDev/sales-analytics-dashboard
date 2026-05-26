"""
data_loader.py
Responsible for loading the CSV and computing all summary metrics.
Every function here takes a DataFrame and returns a simple value or DataFrame.
"""

import pandas as pd


def load_data(filepath="data/sales_data.csv"):
    """Read the CSV and parse the date column so pandas treats it as a date, not a string."""
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df


def get_total_revenue(df):
    """Sum of the total_sales column — the single most important KPI."""
    return df["total_sales"].sum()


def get_top_product(df):
    """Which product generated the most revenue overall?"""
    # Group all rows by product name, sum their sales, find the biggest
    product_sales = df.groupby("product")["total_sales"].sum()
    top = product_sales.idxmax()          # name of the product with max sales
    top_value = product_sales.max()       # its total revenue
    return top, top_value


def get_monthly_trend(df):
    """
    Return total revenue per month as a DataFrame with columns [month, total_sales].
    We extract year-month from the date so Jan 2024 and Jan 2025 stay separate.
    """
    df = df.copy()
    # Create a 'month' column like "2024-01", "2024-02", etc.
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["total_sales"].sum().reset_index()
    return monthly


def get_product_breakdown(df):
    """Total revenue per product — used for the bar chart."""
    breakdown = df.groupby("product")["total_sales"].sum().reset_index()
    breakdown = breakdown.sort_values("total_sales", ascending=False)
    return breakdown


def get_region_breakdown(df):
    """Total revenue per region — used for the pie chart."""
    region = df.groupby("region")["total_sales"].sum().reset_index()
    return region


def get_summary_stats(df):
    """
    Pack all key numbers into a dictionary.
    Calling this once gives app.py everything it needs in one shot.
    """
    total_revenue = get_total_revenue(df)
    top_product, top_product_value = get_top_product(df)
    total_units = df["units_sold"].sum()
    num_transactions = len(df)

    return {
        "total_revenue": total_revenue,
        "top_product": top_product,
        "top_product_value": top_product_value,
        "total_units": total_units,
        "num_transactions": num_transactions,
    }
