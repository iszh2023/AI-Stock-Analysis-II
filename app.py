import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from io import StringIO

# Configure the page
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and professional appearance
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #00D4AA;
    }
    .metric-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #00D4AA;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #FAFAFA;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #00D4AA;
    }
    .error-message {
        background-color: #FF4B4B;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #00D4AA;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def validate_stock_symbol(symbol):
    """Validate if the stock symbol exists and has data"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if 'regularMarketPrice' in info or 'currentPrice' in info:
            return True
        return False
    except:
        return False

def get_stock_data(symbol, period="1y"):
    """Fetch stock data from Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        hist_data = ticker.history(period=period)
        
        # Get company info
        info = ticker.info
        
        # Get financials
        try:
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
        except:
            financials = pd.DataFrame()
            balance_sheet = pd.DataFrame()
            cashflow = pd.DataFrame()
        
        return {
            'history': hist_data,
            'info': info,
            'financials': financials,
            'balance_sheet': balance_sheet,
            'cashflow': cashflow
        }
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def create_price_chart(data, symbol, chart_type="candlestick"):
    """Create interactive price chart using Plotly"""
    fig = go.Figure()
    
    if chart_type == "candlestick":
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=symbol,
            increasing_line_color='#00D4AA',
            decreasing_line_color='#FF4B4B'
        ))
    else:
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name=f'{symbol} Close Price',
            line=dict(color='#00D4AA', width=2)
        ))
    
    fig.update_layout(
        title=f'{symbol} Stock Price',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        template='plotly_dark',
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig

def create_volume_chart(data, symbol):
    """Create volume chart"""
    fig = go.Figure()
    
    colors = ['#00D4AA' if close >= open_price else '#FF4B4B' 
              for close, open_price in zip(data['Close'], data['Open'])]
    
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker_color=colors
    ))
    
    fig.update_layout(
        title=f'{symbol} Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume',
        template='plotly_dark',
        height=300,
        showlegend=False
    )
    
    return fig

def format_large_number(num):
    """Format large numbers with appropriate suffixes"""
    if pd.isna(num) or num is None:
        return "N/A"
    
    if abs(num) >= 1e12:
        return f"${num/1e12:.2f}T"
    elif abs(num) >= 1e9:
        return f"${num/1e9:.2f}B"
    elif abs(num) >= 1e6:
        return f"${num/1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"

def display_key_metrics(info):
    """Display key financial metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        if current_price != 'N/A':
            current_price = f"${current_price:.2f}"
        st.metric("Current Price", current_price)
        
        market_cap = info.get('marketCap', 'N/A')
        if market_cap != 'N/A':
            market_cap = format_large_number(market_cap)
        st.metric("Market Cap", market_cap)
    
    with col2:
        day_change = info.get('regularMarketChange', 'N/A')
        day_change_percent = info.get('regularMarketChangePercent', 'N/A')
        if day_change != 'N/A' and day_change_percent != 'N/A':
            change_str = f"${day_change:.2f} ({day_change_percent*100:.2f}%)"
        else:
            change_str = "N/A"
        st.metric("Day Change", change_str)
        
        volume = info.get('regularMarketVolume', info.get('volume', 'N/A'))
        if volume != 'N/A':
            volume = f"{volume:,}"
        st.metric("Volume", volume)
    
    with col3:
        pe_ratio = info.get('trailingPE', 'N/A')
        if pe_ratio != 'N/A':
            pe_ratio = f"{pe_ratio:.2f}"
        st.metric("P/E Ratio", pe_ratio)
        
        day_high = info.get('dayHigh', 'N/A')
        if day_high != 'N/A':
            day_high = f"${day_high:.2f}"
        st.metric("Day High", day_high)
    
    with col4:
        dividend_yield = info.get('dividendYield', 'N/A')
        if dividend_yield != 'N/A':
            dividend_yield = f"{dividend_yield*100:.2f}%"
        st.metric("Dividend Yield", dividend_yield)
        
        day_low = info.get('dayLow', 'N/A')
        if day_low != 'N/A':
            day_low = f"${day_low:.2f}"
        st.metric("Day Low", day_low)

def convert_df_to_csv(df):
    """Convert dataframe to CSV for download"""
    return df.to_csv().encode('utf-8')

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Stock Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("🔍 Stock Analysis")
        
        # Stock symbol input
        symbol = st.text_input(
            "Enter Stock Symbol",
            value="AAPL",
            help="Enter a valid stock symbol (e.g., AAPL, GOOGL, MSFT)"
        ).upper()
        
        # Time period selection
        period_options = {
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        selected_period = st.selectbox(
            "Select Time Period",
            options=list(period_options.keys()),
            index=3
        )
        
        period = period_options[selected_period]
        
        # Chart type selection
        chart_type = st.radio(
            "Chart Type",
            options=["candlestick", "line"],
            index=0
        )
        
        # Analyze button
        analyze_button = st.button("📊 Analyze Stock", type="primary")
    
    # Main content area
    if analyze_button or symbol:
        if not symbol:
            st.error("Please enter a stock symbol.")
            return
        
        # Validate stock symbol
        with st.spinner("Validating stock symbol..."):
            if not validate_stock_symbol(symbol):
                st.markdown('<div class="error-message">❌ Invalid stock symbol. Please enter a valid stock symbol.</div>', 
                           unsafe_allow_html=True)
                return
        
        # Fetch data
        with st.spinner(f"Fetching data for {symbol}..."):
            stock_data = get_stock_data(symbol, period)
        
        if stock_data is None:
            st.error("Failed to fetch stock data. Please try again.")
            return
        
        if stock_data['history'].empty:
            st.error("No historical data available for this symbol.")
            return
        
        # Display company information
        company_name = stock_data['info'].get('longName', symbol)
        st.markdown(f"## {company_name} ({symbol})")
        
        # Display key metrics
        st.markdown("### 📊 Key Metrics")
        display_key_metrics(stock_data['info'])
        
        # Create two columns for charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Price chart
            st.markdown("### 📈 Price Chart")
            price_chart = create_price_chart(stock_data['history'], symbol, chart_type)
            st.plotly_chart(price_chart, use_container_width=True)
        
        with col2:
            # Volume chart
            st.markdown("### 📊 Volume")
            volume_chart = create_volume_chart(stock_data['history'], symbol)
            st.plotly_chart(volume_chart, use_container_width=True)
        
        # Historical data table
        st.markdown("### 📋 Historical Data")
        
        # Prepare data for display
        display_data = stock_data['history'].copy()
        display_data = display_data.round(2)
        display_data.index = display_data.index.strftime('%Y-%m-%d')
        
        # Show the table
        st.dataframe(display_data, use_container_width=True)
        
        # Download button
        csv_data = convert_df_to_csv(display_data)
        st.download_button(
            label="📥 Download Historical Data as CSV",
            data=csv_data,
            file_name=f"{symbol}_historical_data_{selected_period.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        # Additional company information
        with st.expander("ℹ️ Company Information"):
            info = stock_data['info']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Sector:**", info.get('sector', 'N/A'))
                st.write("**Industry:**", info.get('industry', 'N/A'))
                st.write("**Country:**", info.get('country', 'N/A'))
                st.write("**Employees:**", f"{info.get('fullTimeEmployees', 'N/A'):,}" if info.get('fullTimeEmployees') else 'N/A')
            
            with col2:
                st.write("**Website:**", info.get('website', 'N/A'))
                st.write("**52 Week High:**", f"${info.get('fiftyTwoWeekHigh', 'N/A')}" if info.get('fiftyTwoWeekHigh') else 'N/A')
                st.write("**52 Week Low:**", f"${info.get('fiftyTwoWeekLow', 'N/A')}" if info.get('fiftyTwoWeekLow') else 'N/A')
                st.write("**Beta:**", f"{info.get('beta', 'N/A'):.2f}" if info.get('beta') else 'N/A')
            
            # Business summary
            if 'longBusinessSummary' in info:
                st.write("**Business Summary:**")
                st.write(info['longBusinessSummary'])
    
    else:
        # Welcome message
        st.markdown("""
        ### Welcome to the Stock Analysis Dashboard! 📈
        
        This dashboard provides comprehensive stock analysis with real-time data from Yahoo Finance.
        
        **Features:**
        - 🔍 Real-time stock data and key metrics
        - 📊 Interactive candlestick and line charts
        - 📋 Historical data tables
        - 📥 CSV download functionality
        - 🌙 Professional dark theme
        
        **How to use:**
        1. Enter a stock symbol in the sidebar (e.g., AAPL, GOOGL, MSFT)
        2. Select your preferred time period
        3. Choose between candlestick or line chart
        4. Click "Analyze Stock" to get started
        
        Get started by entering a stock symbol in the sidebar! 👈
        """)

if __name__ == "__main__":
    main()
