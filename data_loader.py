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
    product_sales = df.groupby("product")["total_sales"].sum()
    top = product_sales.idxmax()
    top_value = product_sales.max()
    return top, top_value


def get_monthly_trend(df):
    """Return total revenue per month as a DataFrame with columns [month, total_sales]."""
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["total_sales"].sum().reset_index()
    return monthly


def get_mom_growth(df):
    """
    Month-over-month revenue growth for the most recent month vs the one before it.
    Returns the % change as a float (e.g. 12.5 means +12.5%).
    """
    monthly = get_monthly_trend(df)
    if len(monthly) < 2:
        return 0.0
    last = monthly["total_sales"].iloc[-1]
    prev = monthly["total_sales"].iloc[-2]
    return round(((last - prev) / prev) * 100, 1)


def get_product_breakdown(df):
    """Total revenue per product — used for the bar chart."""
    breakdown = df.groupby("product")["total_sales"].sum().reset_index()
    breakdown = breakdown.sort_values("total_sales", ascending=False)
    return breakdown


def get_region_breakdown(df):
    """Total revenue per region — used for the pie chart."""
    region = df.groupby("region")["total_sales"].sum().reset_index()
    return region


def get_heatmap_data(df):
    """
    Pivot table: rows = products, columns = months, values = revenue.
    Used for the heatmap chart. Shows which product performed best in which month.
    """
    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    pivot = df.pivot_table(
        index="product",
        columns="month",
        values="total_sales",
        aggfunc="sum",
        fill_value=0,
    )
    return pivot


def get_summary_stats(df):
    """
    Pack all key numbers into a dictionary.
    Calling this once gives app.py everything it needs in one shot.
    """
    total_revenue = get_total_revenue(df)
    top_product, top_product_value = get_top_product(df)
    total_units = df["units_sold"].sum()
    num_transactions = len(df)
    mom_growth = get_mom_growth(df)

    return {
        "total_revenue": total_revenue,
        "top_product": top_product,
        "top_product_value": top_product_value,
        "total_units": total_units,
        "num_transactions": num_transactions,
        "mom_growth": mom_growth,
    }
