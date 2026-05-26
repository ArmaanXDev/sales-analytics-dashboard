"""
llm_helper.py
All AI-related logic lives here.
We build a text summary of the data and send it to the Claude API along with the user's question.
"""

import os
import anthropic
from dotenv import load_dotenv

# Load the API key from the .env file into environment variables
load_dotenv()


def _build_data_context(df, stats):
    """
    Convert the DataFrame into a short text block the LLM can read.
    We don't send the full CSV — that would be too long and expensive.
    Instead we send the key facts (totals, top product, monthly peaks).
    This is called 'context injection' — giving the AI only what it needs.
    """
    # Find the best and worst months
    monthly = df.groupby(df["date"].dt.to_period("M").astype(str))["total_sales"].sum()
    best_month = monthly.idxmax()
    worst_month = monthly.idxmin()

    # Revenue per product as a neat string
    product_sales = df.groupby("product")["total_sales"].sum().sort_values(ascending=False)
    product_lines = "\n".join(
        f"  - {p}: ${v:,.0f}" for p, v in product_sales.items()
    )

    # Revenue per region
    region_sales = df.groupby("region")["total_sales"].sum().sort_values(ascending=False)
    region_lines = "\n".join(
        f"  - {r}: ${v:,.0f}" for r, v in region_sales.items()
    )

    context = f"""
Sales Data Summary (January 2024 – December 2024):

- Total Revenue: ${stats['total_revenue']:,.0f}
- Total Units Sold: {stats['total_units']:,}
- Number of Transactions: {stats['num_transactions']}
- Top Product: {stats['top_product']} (${stats['top_product_value']:,.0f})
- Best Month: {best_month}
- Worst Month: {worst_month}

Revenue by Product:
{product_lines}

Revenue by Region:
{region_lines}
"""
    return context.strip()


def answer_question(df, stats, user_question):
    """
    Send the data context + user's question to Claude and return the answer.
    Called when the user clicks 'Get Answer' in the Q&A section.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context = _build_data_context(df, stats)

    prompt = f"""You are a helpful business analyst assistant.
Use ONLY the sales data provided below to answer the question.
Keep your answer concise — 2 to 4 sentences. Do not make up numbers.

{context}

Question: {user_question}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",   # Haiku is fast and cheap — perfect for Q&A
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def generate_insights_summary(df, stats):
    """
    Ask Claude to summarize the main takeaways from the data.
    Called when the user clicks the 'Insights Summary' button.
    Uses a slightly larger token limit because the summary can be longer.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context = _build_data_context(df, stats)

    prompt = f"""You are a business intelligence analyst writing a short executive summary.
Based on the sales data below, write 4 to 5 bullet points highlighting the most important insights.
Focus on trends, standout products, regional performance, and any notable patterns.
Be specific — use the actual numbers from the data.

{context}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
