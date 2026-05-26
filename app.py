"""
app.py  —  Entry point. Run with: streamlit run app.py
This file only handles the UI layout. All logic lives in the other modules.
"""

import streamlit as st
import data_loader
import charts
import llm_helper

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Insights Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Insights Assistant")
st.caption("A simple business analytics dashboard powered by AI")

# ── Load data ─────────────────────────────────────────────────────────────────
# @st.cache_data caches the CSV so it isn't re-read on every UI interaction
@st.cache_data
def load_data():
    return data_loader.load_data()

df = load_data()
stats = data_loader.get_summary_stats(df)

# ── Section 1: Key Metrics ────────────────────────────────────────────────────
st.header("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${stats['total_revenue']:,.0f}",
    )
with col2:
    st.metric(
        label="Top Product",
        value=stats["top_product"],
        delta=f"${stats['top_product_value']:,.0f}",
    )
with col3:
    st.metric(
        label="Total Units Sold",
        value=f"{stats['total_units']:,}",
    )
with col4:
    st.metric(
        label="Total Transactions",
        value=f"{stats['num_transactions']:,}",
    )

st.divider()

# ── Section 2: Charts ─────────────────────────────────────────────────────────
st.header("Sales Charts")

# Monthly trend takes the full width — it's the most important chart
monthly_df = data_loader.get_monthly_trend(df)
st.plotly_chart(charts.monthly_trend_chart(monthly_df), use_container_width=True)

# Product and region charts sit side by side
col_left, col_right = st.columns(2)

with col_left:
    product_df = data_loader.get_product_breakdown(df)
    st.plotly_chart(charts.product_bar_chart(product_df), use_container_width=True)

with col_right:
    region_df = data_loader.get_region_breakdown(df)
    st.plotly_chart(charts.region_pie_chart(region_df), use_container_width=True)

st.divider()

# ── Section 3: AI Q&A ─────────────────────────────────────────────────────────
st.header("Ask a Question About the Data")
st.write("Type any question in plain English — the AI will answer based on the actual sales data.")

user_question = st.text_input(
    label="Your question",
    placeholder="e.g. Which region had the lowest revenue? Which month saw the biggest spike?",
)

if st.button("Get Answer", type="primary"):
    if user_question.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            answer = llm_helper.answer_question(df, stats, user_question)
        st.success("Answer")
        st.write(answer)

st.divider()

# ── Section 4: Insights Summary ───────────────────────────────────────────────
st.header("Insights Summary")
st.write("Click the button below to get an AI-generated summary of the key business takeaways.")

if st.button("Generate Insights Summary", type="secondary"):
    with st.spinner("Generating summary..."):
        summary = llm_helper.generate_insights_summary(df, stats)
    st.info(summary)
