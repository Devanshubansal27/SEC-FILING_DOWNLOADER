from sec_edgar_downloader import Downloader
from datetime import datetime
from pathlib import Path
from enum import Enum

# Define filing types available in SEC EDGAR
class FilingType(str, Enum):
    FORM_10K = "10-K"
    FORM_10Q = "10-Q"
    FORM_8K = "8-K"
    FORM_S1 = "S-1"
    FORM_13F = "13F-HR"
    FORM_4 = "4"
    FORM_DEF14A = "DEF 14A"
    FORM_10KSB = "10-KSB"
    FORM_10QSB = "10-QSB"
    FORM_20F = "20-F"
    FORM_40F = "40-F"
    FORM_6K = "6-K"
    FORM_10 = "10"
    FORM_8A = "8-A"
    FORM_485BPOS = "485BPOS"
    FORM_497 = "497"
    FORM_N1A = "N-1A"
    FORM_N2 = "N-2"
    FORM_NT10K = "NT 10-K"
    FORM_NT10Q = "NT 10-Q"

def get_filing_types():
    """Return a list of available filing types"""
    return [filing.value for filing in FilingType]

def download_edgar_filings(ticker: str, filing_type: str, years_back: int, cik: str = None):
    """
    Download SEC filings for a given ticker, filing type, and years back.
    - Returns a tuple: (success_status, number_of_filings)
    """
    # Set the data directory
    data_dir = Path("edgar_data")
    data_dir.mkdir(exist_ok=True)  # Ensure the data directory exists
    
    # Initialize downloader
    dl = Downloader("MyCompany", "myemail@example.com", data_dir)
    
    # Calculate date ranges based on user input
    today = datetime.now().year
    start_year = today - years_back
    
    try:
        # Determine if we're using a ticker or CIK
        if ticker:
            identifier = ticker
        elif cik:
            identifier = cik
        else:
            raise ValueError("Either a ticker or CIK number must be provided.")
        
        # Download the filings
        try:
            num_downloaded = dl.get(
                filing_type,
                identifier,
                after=f"{start_year}-01-01",
                before=f"{today}-12-31",
                download_details=True
            )
            print(f"Downloaded {num_downloaded} filings")
            
            # Find the directory where filings were downloaded
            filing_dir = data_dir / "sec-edgar-filings" / identifier / filing_type
            print(f"Looking for filings in: {filing_dir}")
            
            if not filing_dir.exists() and num_downloaded > 0:
                print(f"Warning: .get() reported success but directory not found at {filing_dir}")
                return False, 0
                
            return True, num_downloaded
            
        except Exception as e:
            print(f"Error downloading filings: {str(e)}")
            return False, 0
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False, 0