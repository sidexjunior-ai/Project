# Document Sourcing Script - SEC EDGAR + arXiv

A Python utility that combines regulatory filings from SEC EDGAR and academic papers from arXiv into organized directories.

## Features

- **SEC EDGAR Integration**: Downloads 10-K (annual), 10-Q (quarterly), and 8-K (current) filings
- **arXiv Integration**: Searches and downloads academic papers by topic
- **Organized Output**: Structures files into separate SEC_EDGAR and arXiv_Papers folders
- **Error Handling**: Robust exception handling for failed downloads
- **Progress Tracking**: Real-time feedback during downloads

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `document_sourcing.py`:

```python
COMPANY_TICKER = "AAPL"          # Stock ticker
COMPANY_NAME = "Apple Inc"       # Company name
ARXIV_QUERY = "artificial intelligence OR machine learning"
MAX_ARXIV_RESULTS = 5            # Papers to download
```

Update SEC credentials:

```python
dl = Downloader(
    company_name="Your Company Name",
    email_address="your.email@example.com"
)
```

### Run

```bash
python3 document_sourcing.py
```

## Output Structure

```
documents_AAPL_20260510/
├── SEC_EDGAR/
│   └── full-submission.txt (10-K, 10-Q, 8-K filings)
└── arXiv_Papers/
    ├── 01_Watershed_of_Artificial_Intelligence.pdf
    ├── 02_The_Artificial_Scientist.pdf
    └── ...
```

## Configuration Examples

### Tech Stocks
```python
COMPANY_TICKER = "NVDA"
ARXIV_QUERY = "computer vision OR GPU computing OR deep learning"
```

### Financial Data
```python
COMPANY_TICKER = "JPM"
ARXIV_QUERY = "machine learning AND finance"
```

### Healthcare
```python
COMPANY_TICKER = "JNJ"
ARXIV_QUERY = "machine learning AND biomedical"
```

## Requirements

- Python 3.7+
- Internet connection
- Valid SEC credentials (company name and email)

## Status

✅ Fully functional and tested
- SEC EDGAR: 7 filings downloaded
- arXiv: 5 papers downloaded
- Total: 3.8MB of documents