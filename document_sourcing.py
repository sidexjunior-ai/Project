"""
Document Sourcing Script - SEC EDGAR + arXiv
Combines regulatory filings and academic papers
"""

import os
import shutil
from datetime import datetime
from sec_edgar_downloader import Downloader
import arxiv

# ========================= CONFIGURATION =========================
COMPANY_TICKER = "AAPL"          # Change as needed
COMPANY_NAME = "Apple Inc"       # Used for folder naming

# arXiv search query (customize this)
ARXIV_QUERY = "artificial intelligence OR machine learning"  
MAX_ARXIV_RESULTS = 5

# SEC EDGAR configuration
SEC_FILINGS = {
    "10-K": 2,   # Annual reports (limit)
    "10-Q": 2,   # Quarterly reports
    "8-K": 3     # Current reports
}

# Base folder
BASE_DIR = f"documents_{COMPANY_TICKER}_{datetime.now().strftime('%Y%m%d')}"
TEMP_EDGAR_DIR = "sec_temp_downloads"
# ================================================================

def setup_folders():
    """Create organized folder structure"""
    folders = {
        "edgar": os.path.join(BASE_DIR, "SEC_EDGAR"),
        "arxiv": os.path.join(BASE_DIR, "arXiv_Papers")
    }
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    # Clean up temp directory if it exists
    if os.path.exists(TEMP_EDGAR_DIR):
        shutil.rmtree(TEMP_EDGAR_DIR)
    os.makedirs(TEMP_EDGAR_DIR, exist_ok=True)
    
    return folders


def download_edgar_filings(folders):
    """Download SEC filings"""
    print(f"Downloading SEC EDGAR filings for {COMPANY_TICKER}...")
    
    try:
        dl = Downloader(
            company_name="YourCompanyName", 
            email_address="your.email@example.com",  # SEC requires this
            download_folder=TEMP_EDGAR_DIR
        )
        
        # Download filings by type
        for filing_type, limit in SEC_FILINGS.items():
            try:
                print(f"  Downloading {filing_type} (limit: {limit})...")
                dl.get(filing_type, COMPANY_TICKER, limit=limit)
            except Exception as e:
                print(f"  ⚠️  Could not download {filing_type}: {e}")
        
        # Move downloaded files to SEC_EDGAR folder
        edgar_folder = folders["edgar"]
        file_count = 0
        
        for root, dirs, files in os.walk(TEMP_EDGAR_DIR):
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(edgar_folder, file)
                try:
                    shutil.copy2(src_path, dst_path)
                    file_count += 1
                except Exception as e:
                    print(f"  Failed to copy {file}: {e}")
        
        if file_count > 0:
            print(f"✓ Downloaded {file_count} SEC filing(s)")
        else:
            print("⚠️  No SEC filings were downloaded (check credentials)")
            
    except Exception as e:
        print(f"SEC EDGAR download error: {e}")


def download_arxiv_papers(folders):
    """Search and download papers from arXiv"""
    print(f"\nSearching arXiv for: '{ARXIV_QUERY}'...")
    
    client = arxiv.Client()
    search = arxiv.Search(
        query=ARXIV_QUERY,
        max_results=MAX_ARXIV_RESULTS,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    downloaded_count = 0
    
    for i, result in enumerate(client.results(search), 1):
        try:
            # Clean title for filename
            clean_title = "".join(c if c.isalnum() else "_" for c in result.title[:80])
            filename = f"{i:02d}_{clean_title}.pdf"
            
            filepath = os.path.join(folders["arxiv"], filename)
            
            print(f"  Downloading ({i}/{MAX_ARXIV_RESULTS}): {result.title[:65]}...")
            result.download_pdf(dirpath=folders["arxiv"], filename=filename)
            downloaded_count += 1
            
        except Exception as e:
            print(f"  Failed to download paper {i}: {e}")
    
    print(f"✓ Downloaded {downloaded_count} arXiv paper(s)")


if __name__ == "__main__":
    print("🚀 Starting combined document sourcing...\n")
    
    folders = setup_folders()
    
    # Run both downloads
    download_edgar_filings(folders)
    download_arxiv_papers(folders)
    
    # Clean up temp directory
    if os.path.exists(TEMP_EDGAR_DIR):
        shutil.rmtree(TEMP_EDGAR_DIR)
    
    print(f"\n✅ All documents downloaded to: ./{BASE_DIR}/")
    print("   - SEC filings → SEC_EDGAR folder")
    print("   - Academic papers → arXiv_Papers folder")
    print("   - SEC filings → SEC_EDGAR folder")
    print("   - Academic papers → arXiv_Papers folder")
