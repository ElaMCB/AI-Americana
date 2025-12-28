# AI-AMERICANA

A living field-guide to artificial-intelligence activity that is uniquely U.S.-shaped: policy, money, culture, code & myth.

## 1. Why this repo exists

The U.S. is simultaneously the biggest public-sector AI regulator AND the biggest AI venture-capital market.

That tension creates artifacts you don't see elsewhere: Senate "AI Insight Forums," state patchworks (CA SB-1001, TX HB-2273), DOD JADC2 data pipelines, NIST RMF citations in SOC-2 reports, "Godfather of AI" TV specials, etc.

This project tracks those artifacts, turns them into timelines/maps/code, and keeps them in one public git history so researchers & founders don't have to scrape Lexis-Nexis or FedReg every Monday.

## 2. Folder plan

```
/policy/federal          # txt/markdown copies of bills, exec orders, RFIs  
/policy/state            # same, but 50 sub-dirs (start with CA, TX, NY, DC)  
/funding                 # JSON dumps from SBIR, NSF, NIH RePORTER, DIU, In-Q-Tel  
/datasets                # US-open data we actually touch (Census, NOAA, SEC EDGAR)  
/models-made-here        # fine-tunes trained on U.S. gov data + training scripts  
/narratives              # markdown essays linking the above (policy → money → code)  
/media                   # screenshots, maps, d3 html pages  
/archive                 # random PDFs till we decide where they belong  
```

## 3. First 90-day roadmap (turn each line into a GitHub issue)

- [ ] Scrape & parse the 2024-25 U.S. AI executive-order implementation table (OMB M-24-10, DHS guidance, DoD 5000.09) into /policy/federal/executive-orders.md.
- [ ] Build a tiny ETL that pulls weekly SBIR awards matching keyword "artificial intelligence" → JSON in /funding.
- [ ] Fine-tune a 1-B-param model on 2020-24 U.S. Census ACS PUMS data; release weights + reproducible scripts in /models-made-here/census-gpt.
- [ ] Publish a markdown essay: "From the CHIPS Act to Foundry rebates: how U.S. industrial policy is quietly rewriting AI cost curves."
- [ ] Generate an interactive map (Observable / D3) of every federally funded AI R&D center; park source + geoJSON in /media.

## 4. Contributing quickstart

Fork & clone.

We follow the "diary" convention: if you add a primary source, also drop a one-line entry in /changelog.md with date + one-sentence summary.

No binary blobs > 50 MB please—link to GDrive / Zenodo instead.

## 5. License

CC-BY-4.0 for prose & data indexes; MIT for any code under /models-made-here, /scripts, /media/js.

## 2025 update nuggets you can already log

- **Jan 2025**: newly finalized NIST "Generative AI Profile" (NIST AI-100-3) now explicitly references dual-use foundation-model thresholds at 10²⁶ FLOP—add to /policy/federal/nist-ai-profiles.md.
- **DoD 2025 budget mark-up** adds $1.8 B line for "Joint All-Domain Command & Control AI middleware"—good funding JSON to pull when the SF-133s drop.
- **California SB-1001** (AI transparency for ≥10 M users) passed Senate Appropriations 6-1; vote tally & amendment text live in /policy/state/CA/SB-1001_2025.md.

## Next actions for tonight

- [x] Create the folder skeleton above, paste the readme, commit.
- [ ] Open Issue #1: "Scrape & parse 2024-25 EO implementation table."
- [ ] Drop a raw PDF of the latest NIST profile into /policy/federal so the repo has immediate, searchable substance.

From there you can branch, script, write—whatever feels fun. Want a quick Python scraper template for SBIR awards, or a shell one-liner to mirror FedReg AI docs? Let me know and we'll wire it in.
