import streamlit as st
from edgar_downloader import get_filing_types, download_edgar_filings

st.set_page_config(page_title="SEC EDGAR Filings Downloader", layout="centered")
st.title("📄 SEC EDGAR Filings Downloader")

st.markdown("Enter a **company ticker symbol** (e.g., `AAPL`) or a **CIK number** (e.g., `320193`).")

# Combined input for ticker or CIK
user_input = st.text_input("Enter Ticker or CIK").strip()

filing_type = st.selectbox("Select Filing Type", get_filing_types())
years_back = st.slider("How many years back do you want to fetch filings?", 1, 20, 5)

# Button to trigger download
if st.button("📥 Download Filings"):
    if not user_input:
        st.warning("⚠️ Please enter a ticker symbol or a CIK.")
    else:
        # Determine if input is CIK (all digits) or ticker (contains letters)
        if user_input.isdigit():
            ticker = None
            cik = user_input
        else:
            ticker = user_input.upper()
            cik = None

        with st.spinner("Downloading filings..."):
            success, count = download_edgar_filings(
                ticker=ticker,
                cik=cik,
                filing_type=filing_type,
                years_back=years_back
            )
            if success:
                st.success(f"✅ Successfully downloaded {count} filings.")
            else:
                st.error("❌ Failed to download filings. Check your input and try again.")
