import streamlit as st
from pathlib import Path
import shutil
from edgar_downloader import get_filing_types, download_edgar_filings

st.set_page_config(page_title="EDGAR Filings Downloader", layout="centered")
st.title("📦 SEC EDGAR Filings Downloader")

st.markdown("Enter a **Ticker** (e.g. `AAPL`) or a **CIK** (e.g. `320193`) and download filings as a ZIP.")

user_input = st.text_input("Ticker or CIK").strip()
filing_type = st.selectbox("Select Filing Type", get_filing_types())
years_back = st.slider("Years Back", 1, 20, 5)

# ⛔ DO NOT CALL download_edgar_filings OUTSIDE THE BUTTON
# This avoids crash on app load or refresh

if st.button("📥 Download ZIP"):
    if not user_input:
        st.warning("⚠️ Please enter a ticker or CIK.")
    else:
        ticker, cik = (None, user_input) if user_input.isdigit() else (user_input.upper(), None)

        with st.spinner("Fetching filings and zipping..."):
            success, count, data_dir = download_edgar_filings(
                ticker=ticker,
                cik=cik,
                filing_type=filing_type,
                years_back=years_back
            )

            if success and count > 0:
                zip_path = shutil.make_archive("edgar_filings", 'zip', data_dir)

                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download ZIP",
                        data=f,
                        file_name="edgar_filings.zip",
                        mime="application/zip"
                    )
            else:
                st.error("❌ Could not fetch filings. Check the ticker/CIK or try again later.")
