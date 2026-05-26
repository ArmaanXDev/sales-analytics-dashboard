# 📊 Sales Insights Assistant

An interactive business analytics dashboard built with Python and Streamlit. Load a sales dataset, explore key metrics through dynamic charts, and filter data by region, product, and date — all in real time.

---

## Features

- **KPI Cards** — Total revenue, top product, units sold, transactions, and month-over-month growth
- **Monthly Trend Chart** — Line chart showing revenue across all 12 months
- **Product Revenue Bar Chart** — Horizontal bar chart comparing all products
- **Regional Pie Chart** — Revenue split across North, South, East, and West
- **Revenue Heatmap** — Product × Month grid showing which product performed best when
- **Sidebar Filters** — Filter by region, product, and date range; all charts update instantly
- **Data Explorer** — Sortable table of filtered transactions with a one-click CSV download

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web app framework — Python only, no HTML/CSS needed |
| [pandas](https://pandas.pydata.org) | Data loading and metric calculations |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Secure environment variable management |

---

## Project Structure

```
├── app.py              # Main Streamlit app — UI layout only
├── data_loader.py      # CSV loading and all metric calculations
├── charts.py           # Plotly chart functions
├── data/
│   └── sales_data.csv  # Sample dataset (150 rows, 5 products, 4 regions, 2024)
├── requirements.txt    # Python dependencies
└── .env                # API keys — not committed to git
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/ArmaanXDev/sales-insights-assistant.git
cd sales-insights-assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

---

## Screenshots

> Dashboard with sidebar filters, KPI metrics, and interactive charts.

---

## Dataset

The included `data/sales_data.csv` contains 150 synthetic transactions across:
- **5 Products** — Laptop, Phone, Tablet, Headphones, Monitor
- **4 Regions** — North, South, East, West
- **12 Months** — January to December 2024

---

## Author

**Armaan Sharma**  
[GitHub](https://github.com/ArmaanXDev)
