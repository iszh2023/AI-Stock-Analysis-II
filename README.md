# 📈 Stock Analysis Dashboard

A modern, interactive **stock analysis web application** built with Streamlit and powered by **real-time Yahoo Finance data**.

This project is an enhanced upgrade of the previous version — now more accurate, more responsive, and visually polished.

## 🚀 Features

- 🔍 **Real-time stock price and key metrics**
- 🕯 **Candlestick & line chart visualization**
- 🗓 **Flexible time-range selection**
- 🗃 **Historical OHLCV data table**
- 💾 **CSV download support**
- 🌙 **Stylish dark theme**
- ℹ️ **Company information panel**

## 🖼️ Screenshots

### 🏠 Dashboard Home
![Dashboard Screenshot](images/dashboard.png)

### 📋 Historical Data
![Historical Data Screenshot](images/historical.png)

### 📈 Key Metrics
![Key Metrics Screenshot](images/metrics.png)

### 🕯️ Price & Volume Charts
![Charts Screenshot](images/charts.png)

*(After uploading screenshots, update the file names above.)*

## 📚 What This App Does

This Streamlit dashboard allows you to:

### ✔ Search any stock ticker
Examples: `AAPL`, `GOOGL`, `TSLA`, `MSFT`.

### ✔ Choose analysis duration
1 month → multiple years.

### ✔ Switch chart styles
- Candlestick (trading-focused)
- Line chart (trend-focused)

### ✔ View complete market information
Includes:
- Current price
- Market cap
- Day high / low
- Volume
- Price change (absolute + %)
- Dividend yield
- P/E ratio

### ✔ Analyze price movement visually
Interactive Plotly charts support:
- Hover values
- Zoom
- Pan
- Crosshair inspection

### ✔ Read and export historical data
Daily OHLCV + dividends + stock splits
Downloadable as CSV.

## 🧩 Tech Stack

- **Python 3**
- **Streamlit**
- **yfinance**
- **Plotly**
- **pandas**
- `uv` / `pyproject.toml` dependency management

## ▶️ Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Using `uv`:

```bash
uv sync
uv run streamlit run app.py
```

## 📄 License

Apache-2.0
