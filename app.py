"""
app.py  —  Entry point. Run with: streamlit run app.py
This file only handles the UI layout. All logic lives in the other modules.
"""

import streamlit as st
import pandas as pd
import data_loader
import charts

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# Custom CSS — tighten metric card borders for a cleaner enterprise look
st.markdown("""
    <style>
        [data-testid="metric-container"] {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 16px;
        }
        .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive business analytics dashboard — 2024 Sales Data")

# ── Load full dataset once (cached) ──────────────────────────────────────────
@st.cache_data
def load_data():
    return data_loader.load_data()

full_df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
# The sidebar is what separates a basic script from a real BI tool.
# Every selection here instantly updates all charts and metrics below.
with st.sidebar:
    st.header("Filters")

    all_regions = sorted(full_df["region"].unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
    )

    all_products = sorted(full_df["product"].unique().tolist())
    selected_products = st.multiselect(
        "Product",
        options=all_products,
        default=all_products,
    )

    min_date = full_df["date"].min().date()
    max_date = full_df["date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.divider()
    st.caption("Filters apply to all charts and metrics.")

# Apply filters to create the working DataFrame
# We only filter by date if the user selected both start and end
if len(date_range) == 2:
    start_date, end_date = date_range
    df = full_df[
        (full_df["region"].isin(selected_regions)) &
        (full_df["product"].isin(selected_products)) &
        (full_df["date"].dt.date >= start_date) &
        (full_df["date"].dt.date <= end_date)
    ]
else:
    df = full_df[
        (full_df["region"].isin(selected_regions)) &
        (full_df["product"].isin(selected_products))
    ]

# Guard against empty selection
if df.empty:
    st.warning("No data matches the selected filters. Adjust the sidebar.")
    st.stop()

stats = data_loader.get_summary_stats(df)

# ── Section 1: KPI Metrics ────────────────────────────────────────────────────
st.header("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Revenue", f"${stats['total_revenue']:,.0f}")

with col2:
    st.metric(
        "Top Product",
        stats["top_product"],
        delta=f"${stats['top_product_value']:,.0f}",
    )

with col3:
    st.metric("Total Units Sold", f"{stats['total_units']:,}")

with col4:
    st.metric("Total Transactions", f"{stats['num_transactions']:,}")

with col5:
    st.metric(
        "MoM Revenue Growth",
        f"{stats['mom_growth']:+.1f}%",
        delta=f"{stats['mom_growth']:+.1f}%",
    )

st.divider()

# ── Section 2: Trend & Breakdown Charts ──────────────────────────────────────
st.header("Revenue Analysis")

monthly_df = data_loader.get_monthly_trend(df)
st.plotly_chart(charts.monthly_trend_chart(monthly_df), use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    product_df = data_loader.get_product_breakdown(df)
    st.plotly_chart(charts.product_bar_chart(product_df), use_container_width=True)

with col_right:
    region_df = data_loader.get_region_breakdown(df)
    st.plotly_chart(charts.region_pie_chart(region_df), use_container_width=True)

st.divider()

# ── Section 3: Heatmap ────────────────────────────────────────────────────────
st.header("Product Performance Heatmap")
st.caption("Darker = higher revenue. Quickly spot which product dominated which month.")

pivot_df = data_loader.get_heatmap_data(df)
st.plotly_chart(charts.heatmap_chart(pivot_df), use_container_width=True)

st.divider()

# ── Section 4: Raw Data Explorer ─────────────────────────────────────────────
st.header("Data Explorer")

col_search, col_download = st.columns([3, 1])

with col_search:
    st.caption(f"Showing {len(df):,} transactions matching current filters.")

with col_download:
    # Convert DataFrame to CSV bytes so Streamlit can serve it as a file download
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_bytes,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

# Show the filtered table — st.dataframe is interactive (sortable, scrollable)
st.dataframe(
    df.sort_values("date", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=300,
)
