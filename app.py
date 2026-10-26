import streamlit as st
import ccxt
import pandas as pd

st.set_page_config(
    page_title="Futures Screener",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Crypto Futures Screener")
st.caption("Binance Futures + Bybit Futures")

exchange_name = st.selectbox(
    "Pilih Exchange",
    ["Binance Futures", "Bybit Futures"]
)

if st.button("🔄 Load Markets", use_container_width=True):

    try:
        if exchange_name == "Binance Futures":
            exchange = ccxt.binance({
                "options": {
                    "defaultType": "future"
                }
            })
        else:
            exchange = ccxt.bybit({
                "options": {
                    "defaultType": "linear"
                }
            })

        with st.spinner("Mengambil market futures..."):
            markets = exchange.load_markets()

        rows = []

        for symbol, market in markets.items():
            if not market.get("active"):
                continue

            if market.get("contract") and market.get("linear"):
                rows.append({
                    "Symbol": symbol,
                    "Base": market.get("base"),
                    "Quote": market.get("quote"),
                    "Type": market.get("type"),
                })

        df = pd.DataFrame(rows)

        st.success(f"Berhasil! {len(df)} market futures ditemukan.")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Error: {type(e).__name__}")
        st.code(str(e))