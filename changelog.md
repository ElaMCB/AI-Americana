# Changelog

This file tracks primary sources and significant updates added to the repository.

## 2025-01-XX

- Initial repository structure created with folder skeleton (policy/federal, policy/state, funding, datasets, models-made-here, narratives, media, archive)
- Added scraper templates and ETL scripts:
  - `scripts/sbir_scraper.py`: Python scraper for SBIR awards matching "artificial intelligence" keyword
  - `scripts/fedreg_scraper.sh`: Bash script for mirroring Federal Register AI documents
  - `scripts/fedreg_scraper.ps1`: PowerShell version of FedReg scraper
  - `scripts/funding_etl.py`: Complete ETL pipeline for funding data from SBIR, NSF, NIH RePORTER, and DIU sources
  - `scripts/requirements.txt`: Python dependencies for scripts
  - `scripts/README.md`: Documentation for all scripts

