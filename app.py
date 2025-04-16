import streamlit as st
from pathlib import Path
import shutil
import os
from edgar_downloader import get_filing_types, download_edgar_filings

st.set_page_config(page_title="SEC Filings Downloader", layout="centered")
st.title("📦 SEC Filings Downloader")

st.markdown("Enter a **Ticker** (e.g. `AAPL`) or a **CIK** (e.g. `320193`) and download filings as a ZIP.")

user_input = st.text_input("Ticker or CIK").strip()
filing_type = st.selectbox("Select Filing Type", get_filing_types())
years_back = st.slider("Years Back", 1, 20, 5)

if st.button("📥 Fetch Filings"):
    if not user_input:
        st.warning("⚠️ Please enter a ticker or CIK.")
    else:
        # Determine input type: if all digits, consider as CIK, else a ticker.
        ticker, cik = (None, user_input) if user_input.isdigit() else (user_input.upper(), None)
        
        # Clear previous downloads so only current filings appear in the ZIP.
        if os.path.exists("edgar_data"):
            shutil.rmtree("edgar_data")
        Path("edgar_data").mkdir(exist_ok=True)
        
        with st.spinner("Fetching filings and creating ZIP..."):
            try:
                success, count, data_dir = download_edgar_filings(
                    ticker=ticker,
                    cik=cik,
                    filing_type=filing_type,
                    years_back=years_back
                )

                # If no filings are found, show an error message.
                if not success or count == 0:
                    st.error("❌ No filings found. Please provide a correct ticker name or CIK number.")
                else:
                    zip_path = shutil.make_archive("edgar_filings", 'zip', data_dir)
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download ZIP",
                            data=f,
                            file_name="edgar_filings.zip",
                            mime="application/zip"
                        )
            except Exception as e:
                st.error(f"💥 Something went wrong:\n\n`{str(e)}`")
