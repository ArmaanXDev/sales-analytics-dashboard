"""
charts.py
Each function creates and returns one Plotly chart.
app.py calls these and passes the result to st.plotly_chart().
"""

import plotly.express as px


def monthly_trend_chart(monthly_df):
    """Line chart showing how revenue changed month by month."""
    fig = px.line(
        monthly_df,
        x="month",
        y="total_sales",
        title="Monthly Revenue Trend",
        labels={"month": "Month", "total_sales": "Revenue ($)"},
        markers=True,          # show a dot at each data point
    )
    fig.update_layout(xaxis_tickangle=-45)   # tilt labels so they don't overlap
    return fig


def product_bar_chart(product_df):
    """Horizontal bar chart — easiest way to compare products at a glance."""
    fig = px.bar(
        product_df,
        x="total_sales",
        y="product",
        orientation="h",       # horizontal bars
        title="Revenue by Product",
        labels={"total_sales": "Revenue ($)", "product": "Product"},
        color="total_sales",   # gradient color by value — makes it visually clear
        color_continuous_scale="Blues",
    )
    return fig


def region_pie_chart(region_df):
    """Pie chart for regional revenue split."""
    fig = px.pie(
        region_df,
        names="region",
        values="total_sales",
        title="Revenue by Region",
        hole=0.3,              # donut style — looks cleaner than a full pie
    )
    return fig
