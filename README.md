# AI-AMERICANA

<!-- AI-Americana badge bar -->
![Repo status](https://img.shields.io/badge/status-🌱%20WIP-yellow)
![GitHub last commit](https://img.shields.io/github/last-commit/ElaMCB/AI-Americana?color=success)
![GitHub repo size](https://img.shields.io/github/repo-size/ElaMCB/AI-Americana)
![License](https://img.shields.io/github/license/ElaMCB/AI-Americana?color=blue)
![Language](https://img.shields.io/github/languages/top/ElaMCB/AI-Americana?color=%23ff69b4)
![US models](https://img.shields.io/badge/US%20models-🇺🇸-red)
![open-source](https://img.shields.io/badge/open-source-✓-brightgreen)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

A living field-guide to artificial-intelligence activity that is uniquely U.S.-shaped: policy, money, culture, code & myth.

## 1. Why this repo exists

The U.S. is simultaneously the biggest public-sector AI regulator AND the biggest AI venture-capital market.

That tension creates artifacts not seen elsewhere: Senate "AI Insight Forums," state patchworks (CA SB-1001, TX HB-2273), DOD JADC2 data pipelines, NIST RMF citations in SOC-2 reports, "Godfather of AI" TV specials, etc.

This project tracks those artifacts, turns them into timelines/maps/code, and keeps them in one public git history so researchers & founders don't have to scrape Lexis-Nexis or FedReg every Monday.

## 2. Folder plan

```
/policy/federal          # txt/markdown copies of bills, exec orders, RFIs  
/policy/state            # same, but 50 sub-dirs (start with CA, TX, NY, DC)  
/funding                 # JSON dumps from SBIR, NSF, NIH RePORTER, DIU, In-Q-Tel  
/datasets                # US-open data used in this project (Census, NOAA, SEC EDGAR)  
/models-made-here        # fine-tunes trained on U.S. gov data + training scripts  
/narratives              # markdown essays linking the above (policy → money → code)  
/media                   # screenshots, maps, d3 html pages  
/archive                 # temporary storage for documents pending categorization  
```

## 3. Contributing quickstart

Fork & clone.

This project follows the "diary" convention: when adding a primary source, include a one-line entry in /changelog.md with date + one-sentence summary.

No binary blobs > 50 MB please—link to GDrive / Zenodo instead.

## 4. 2025 update nuggets ready to log

- **Jan 2025**: newly finalized NIST "Generative AI Profile" (NIST AI-100-3) now explicitly references dual-use foundation-model thresholds at 10²⁶ FLOP—add to /policy/federal/nist-ai-profiles.md.
- **DoD 2025 budget mark-up** adds $1.8 B line for "Joint All-Domain Command & Control AI middleware"—good funding JSON to pull when the SF-133s drop.
- **California SB-1001** (AI transparency for ≥10 M users) passed Senate Appropriations 6-1; vote tally & amendment text live in /policy/state/CA/SB-1001_2025.md.

## 5. License

CC-BY-4.0 for prose & data indexes; MIT for any code under /models-made-here, /scripts, /media/js.

