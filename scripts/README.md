# Scripts

This directory contains scripts for data collection, scraping, and ETL operations.

## Scripts Overview

### `sbir_scraper.py`
Python scraper for SBIR (Small Business Innovation Research) awards matching "artificial intelligence" keyword.

**Usage:**
```bash
python scripts/sbir_scraper.py --keyword "artificial intelligence" --limit 1000
```

**Features:**
- Fetches from SBIR.gov API (adjust endpoint as needed)
- Web scraping fallback option
- Filters for AI-relevant awards
- Saves to JSON format in `/funding` directory

**Note:** You may need to adjust API endpoints based on actual SBIR.gov API documentation.

### `fedreg_scraper.sh` / `fedreg_scraper.ps1`
Scripts for mirroring Federal Register AI-related documents (Bash and PowerShell versions).

**Usage (Bash):**
```bash
chmod +x scripts/fedreg_scraper.sh
./scripts/fedreg_scraper.sh
```

**Usage (PowerShell):**
```powershell
.\scripts\fedreg_scraper.ps1
```

**Features:**
- Uses Federal Register API
- Searches multiple AI-related keywords
- Extracts individual documents as markdown
- Creates index file
- Rate limiting built-in

**Dependencies:**
- **Bash version**: `curl` (required), `jq` (optional, for JSON parsing)
- **PowerShell version**: Native PowerShell cmdlets (no external dependencies)

**Note:** Use the PowerShell version on Windows for better compatibility.

### `funding_etl.py`
Complete ETL pipeline for funding data from multiple U.S. sources (SBIR, NSF, NIH RePORTER, DIU).

**Usage:**
```bash
# Extract from specific sources
python scripts/funding_etl.py --sources sbir nsf --keyword "artificial intelligence"

# Extract from all sources
python scripts/funding_etl.py --sources all --format json
```

**Features:**
- Multi-source extraction (SBIR, NSF, NIH, DIU)
- Data standardization/transformation
- Multiple output formats (JSON, CSV, Parquet)
- Combined dataset generation
- Rate limiting and error handling

**Output:**
- Individual source files in `/funding` directory
- Combined dataset with all sources
- Standardized schema across all sources

## Setup

1. Install Python dependencies:
```bash
pip install -r scripts/requirements.txt
```

2. For shell scripts on Windows:
   - Use Git Bash, or
   - Use WSL (Windows Subsystem for Linux), or
   - Convert to PowerShell equivalent

3. Configure API endpoints:
   - Review and adjust API endpoints in scripts based on actual API documentation
   - Some APIs may require authentication (add API keys as environment variables)

## Data Sources

- **SBIR**: https://www.sbir.gov/
- **NSF**: https://www.nsf.gov/awardsearch/
- **NIH RePORTER**: https://api.reporter.nih.gov/
- **Federal Register**: https://www.federalregister.gov/api/v1/documents
- **DIU**: Defense Innovation Unit (may require SAM.gov API or FOIA requests)

## Notes

- These scripts are templates and may need adjustment based on actual API structures
- Respect rate limits and terms of service for each data source
- Some APIs may require registration or API keys
- Large datasets should be stored externally (see main README)

## License

MIT (as specified in main repository license for code)

