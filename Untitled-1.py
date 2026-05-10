"""
Document Sourcing Script - SEC EDGAR + arXiv
Combines regulatory filings and academic papers
"""

import os
from datetime import datetime
from sec_edgar_downloader import Downloader
import arxiv

# ========================= CONFIGURATION =========================
COMPANY_TICKER = "AAPL"          # Change as needed
COMPANY_NAME = "Apple Inc"       # Used for folder naming

# arXiv search query (customize this)
ARXIV_QUERY = "artificial intelligence OR machine learning"  
MAX_ARXIV_RESULTS = 5

# Base folder
BASE_DIR = f"documents_{COMPANY_TICKER}_{datetime.now().strftime('%Y%m%d')}"
# ================================================================

def setup_folders():
    """Create organized folder structure"""
    folders = {
        "edgar": os.path.join(BASE_DIR, "SEC_EDGAR"),
        "arxiv": os.path.join(BASE_DIR, "arXiv_Papers")
    }
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    return folders


def download_edgar_filings():
    """Download SEC filings"""
    print(f"Downloading SEC EDGAR filings for {COMPANY_TICKER}...")
    
    dl = Downloader(
        company_name="YourCompanyName", 
        email_address="your.email@example.com"  # SEC requires this
    )
    
    # Download recent 10-K and 10-Q
    dl.get("10-K", COMPANY_TICKER, limit=2)
    dl.get("10-Q", COMPANY_TICKER, limit=2)
    dl.get("8-K", COMPANY_TICKER, limit=3)
    
    print("✓ EDGAR filings downloaded successfully!")


def download_arxiv_papers():
    """Search and download papers from arXiv"""
    print(f"\nSearching arXiv for: '{ARXIV_QUERY}'...")
    
    search = arxiv.Search(
        query=ARXIV_QUERY,
        max_results=MAX_ARXIV_RESULTS,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    for i, result in enumerate(search.results(), 1):
        try:
            # Clean title for filename
            clean_title = "".join(c if c.isalnum() else "_" for c in result.title[:80])
            filename = f"{i:02d}_{clean_title}.pdf"
            
            filepath = os.path.join(folders["arxiv"], filename)
            
            print(f"Downloading ({i}/{MAX_ARXIV_RESULTS}): {result.title[:70]}...")
            result.download_pdf(dirpath=folders["arxiv"], filename=filename)
            
        except Exception as e:
            print(f"Failed to download paper {i}: {e}")


if __name__ == "__main__":
    print("🚀 Starting combined document sourcing...\n")
    
    folders = setup_folders()
    
    # Run both downloads
    download_edgar_filings()
    download_arxiv_papers()
    
    print(f"\n✅ All documents downloaded to: ./{BASE_DIR}/")
    print("   - SEC filings → SEC_EDGAR folder")
    print("   - Academic papers → arXiv_Papers folder")
    python document_sourcer.py
    