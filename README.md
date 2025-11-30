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
<img width="2858" height="1534" alt="image" src="https://github.com/user-attachments/assets/a3658dd2-c8f4-48b4-a6be-8ab442df808d" />

### 📋 Historical Data
<img width="2090" height="1368" alt="image" src="https://github.com/user-attachments/assets/c63a67d7-52bc-4e0b-97c0-a6082ffcdc27" />



### 📈 Key Metrics
<img width="941" height="402" alt="Screenshot 2025-11-29 at 4 55 28 PM" src="https://github.com/user-attachments/assets/af29a7bf-e1aa-4cb4-8c9c-d6c5ec520b07" />


### 🕯️ Price & Volume Charts
<img width="2198" height="1194" alt="image" src="https://github.com/user-attachments/assets/8b9ea6a6-5839-4fc2-a1bc-100bb9e8c8d9" />


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



📄 Apache-2.0 License
