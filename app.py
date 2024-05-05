import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Set page config to adjust title, set favicon, and add description for SEO
st.set_page_config(
    page_title="Stock Comparison Dashboard",
    page_icon="📊",  # Using an emoji for the favicon, you can choose any other or use an image
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This Stock Comparison Dashboard helps users compare annual stock returns across various sectors. Easily visualize performance differences and make informed investment decisions."
    }
)

# Optionally, add meta tags for SEO using HTML
meta_tags_html = """
<meta name="description" content="Use the Stock Comparison Dashboard to compare annual stock returns across various industries. Ideal for investors and financial analysts looking to make data-driven decisions.">
<meta name="keywords" content="stock comparison, annual returns, financial analysis, investment decision, stock performance">
"""
st.markdown(meta_tags_html, unsafe_allow_html=True)

# Your main app goes here
st.title("Stock Comparison Dashboard")

# Example content
st.write("Explore stock performance by sector and discover investment opportunities.")


def get_annual_return(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    if not hist.empty:
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        return (end_price - start_price) / start_price * 100  # Return percentage
    else:
        return None

# Initialize the conversation state to store messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def send_message(message_type, message):
    st.session_state['messages'].append((message_type, message))

def clear_messages():
    st.session_state['messages'] = []

def chat_interface():
    st.sidebar.title("Compare Wins by Sector")
    sectors = {
        "Food": "KHC,MDLZ,GIS,CPB,TSN",
        "Technology": "AAPL,MSFT,GOOGL,IBM,META",
        "Semiconductors (Chips)": "AMD,NVDA,TSM,ASML,QCOM",
        "Cement": "CX,EXP,CRH,MLM,JHX",
        "Finance": "JPM,BAC,C,WFC,GS",
        "Water": "AWK,CTWS,CWT,PNNW,WTRG",
        "Import/Export": "ZNH,CPA,EXPD,ZNH,SINO",
        "Insurance": "AFL,ALL,TRV,MET,PGR",
        "Automobile": "F,TM,HMC,GM,VWAGY"
    }

    for sector, stocks in sectors.items():
        st.sidebar.markdown(f"**{sector}:**")
        if st.sidebar.button(stocks):
            st.session_state.input = stocks
            process_input(stocks)

    user_input = st.text_input("Enter stock symbols separated by commas (e.g., 'IBM,AAPL,GOOGL') to compare their annual returns:", key="input")

    # When the user submits ticker symbols
    if st.session_state.input:
        process_input(user_input.upper())

def process_input(input_string):
    tickers = input_string.split(',')
    results = {}
    for ticker in tickers:
        ticker = ticker.strip()
        annual_return = get_annual_return(ticker)
        if annual_return is not None:
            results[ticker] = annual_return
        else:
            results[ticker] = "No data available"
    plot_returns(results)
    send_message('user', f"Comparing annual returns for: {', '.join(tickers)}")
    # Clear input box after processing
    del st.session_state.input

def plot_returns(returns):
    if all(isinstance(val, str) for val in returns.values()):
        send_message('bot', "No valid data to display.")
        return

    fig, ax = plt.subplots()
    stocks, gains = zip(*[(k, v) if not isinstance(v, str) else (k, 0) for k, v in returns.items()])
    ax.bar(stocks, gains, color='green')
    ax.set_ylabel('Annual Return (%)')
    ax.set_title('Annual Returns Comparison')
    for i, v in enumerate(gains):
        ax.text(i, v + (1 if v >= 0 else -4), f"{v:.2f}%", ha='center', color='black')

    st.pyplot(fig)
    send_message('bot', "Bar chart showing annual returns.")

def main():
    st.title("Compare Stocks by Annual Wins with Charts")
    st.success("Stocks Comparing by Annual Wins. Free Time Saver for Stock Traders to make better Decisions.")

    if st.button("Clear Chat"):
        clear_messages()

    chat_container = st.container()
    with chat_container:
        for message_type, message in st.session_state.messages:
            if message_type == 'user':
                st.text_area("", value=message, height=25, key=f"user_{message}", disabled=True)
            elif message_type == 'bot':
                if message == "Bar chart showing annual returns.":
                    continue  # Skip plotting text for chart
                st.text_area("", value=message, height=50, key=f"bot_{message}", disabled=True)


    chat_interface()

    st.markdown("Github: [Streamlit Finance by pacnimo](https://github.com/pacnimo/streamlit_finance)", unsafe_allow_html=True)
if __name__ == "__main__":
    main()

