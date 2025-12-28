#!/usr/bin/env python3
"""
Funding Data ETL Pipeline
Extracts, transforms, and loads funding data from multiple U.S. sources.
Sources: SBIR, NSF, NIH RePORTER, DIU, In-Q-Tel
"""

import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse
import time

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "funding"
OUTPUT_DIR.mkdir(exist_ok=True)

class FundingETL:
    """ETL pipeline for U.S. AI funding data."""
    
    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_sbir(self, keyword: str = "artificial intelligence") -> List[Dict]:
        """Extract SBIR awards data."""
        print("Extracting SBIR awards...")
        # Import the SBIR scraper functionality
        import sys
        from pathlib import Path
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))
        
        try:
            from sbir_scraper import fetch_sbir_api, filter_ai_relevant
            awards = fetch_sbir_api(keyword)
            filtered = filter_ai_relevant(awards, keyword)
            return filtered
        except ImportError:
            print("  Warning: Could not import sbir_scraper, using direct API call")
            # Fallback: direct API call logic here
            return []
    
    def extract_nsf(self, keyword: str = "artificial intelligence") -> List[Dict]:
        """Extract NSF grants data from NSF Awards API."""
        print("Extracting NSF grants...")
        grants = []
        
        # NSF Awards API endpoint (check actual API documentation)
        api_url = "https://api.nsf.gov/services/v1/awards.json"
        
        try:
            params = {
                "keyword": keyword,
                "dateStart": "2020-01-01",  # Adjust date range as needed
                "dateEnd": datetime.now().strftime("%Y-%m-%d"),
                "limit": 1000
            }
            
            response = requests.get(api_url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Adjust parsing based on actual NSF API response
                if "response" in data and "award" in data["response"]:
                    grants = data["response"]["award"]
        except Exception as e:
            print(f"  NSF API extraction failed: {e}")
            print("  Note: NSF API structure may differ - check documentation")
        
        return grants
    
    def extract_nih(self, keyword: str = "artificial intelligence") -> List[Dict]:
        """Extract NIH grants from RePORTER API."""
        print("Extracting NIH grants from RePORTER...")
        grants = []
        
        # NIH RePORTER API endpoint
        api_url = "https://api.reporter.nih.gov/v2/projects/search"
        
        try:
            payload = {
                "criteria": {
                    "advanced_text_search": {
                        "search_text": keyword
                    },
                    "fiscal_years": [2020, 2021, 2022, 2023, 2024, 2025]
                },
                "offset": 0,
                "limit": 1000
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    grants = data["results"]
        except Exception as e:
            print(f"  NIH RePORTER extraction failed: {e}")
            print("  Note: NIH API may require authentication or have rate limits")
        
        return grants
    
    def extract_diu(self) -> List[Dict]:
        """Extract DIU (Defense Innovation Unit) contract data."""
        print("Extracting DIU contracts...")
        contracts = []
        
        # DIU data may be available via SAM.gov or their website
        # This is a template - adjust based on actual data source
        try:
            # Example: SAM.gov API or web scraping
            # sam_api = "https://api.sam.gov/opportunities/v2/search"
            print("  DIU extraction not yet implemented")
            print("  Consider: SAM.gov API, FOIA requests, or web scraping")
        except Exception as e:
            print(f"  DIU extraction failed: {e}")
        
        return contracts
    
    def transform_funding_data(self, raw_data: List[Dict], source: str) -> pd.DataFrame:
        """Transform raw funding data into standardized format."""
        print(f"Transforming {source} data...")
        
        standardized = []
        for item in raw_data:
            # Map different API formats to common schema
            standardized_item = {
                "source": source,
                "id": item.get("id") or item.get("award_id") or item.get("contract_number"),
                "title": item.get("title") or item.get("project_title") or item.get("name"),
                "organization": item.get("organization") or item.get("recipient") or item.get("company"),
                "amount": self._extract_amount(item),
                "start_date": item.get("start_date") or item.get("award_date") or item.get("date"),
                "end_date": item.get("end_date") or item.get("completion_date"),
                "agency": item.get("agency") or item.get("sponsor") or source.upper(),
                "description": item.get("description") or item.get("abstract") or item.get("summary"),
                "url": item.get("url") or item.get("link") or item.get("html_url"),
                "raw_data": item  # Keep original for reference
            }
            standardized.append(standardized_item)
        
        return pd.DataFrame(standardized)
    
    def _extract_amount(self, item: Dict) -> Optional[float]:
        """Extract monetary amount from various field names."""
        amount_fields = ["amount", "award_amount", "total_amount", "value", "budget"]
        for field in amount_fields:
            if field in item:
                amount = item[field]
                if isinstance(amount, (int, float)):
                    return float(amount)
                elif isinstance(amount, str):
                    # Remove currency symbols and commas
                    cleaned = amount.replace("$", "").replace(",", "").strip()
                    try:
                        return float(cleaned)
                    except ValueError:
                        continue
        return None
    
    def load_funding_data(self, df: pd.DataFrame, source: str, format: str = "json") -> Path:
        """Load transformed funding data to storage."""
        print(f"Loading {source} data to {format} format...")
        
        timestamp = datetime.now().strftime("%Y%m%d")
        base_filename = f"{source}_funding_{timestamp}"
        
        if format == "json":
            output_path = self.output_dir / f"{base_filename}.json"
            df.to_json(output_path, orient="records", indent=2, date_format="iso")
        elif format == "csv":
            output_path = self.output_dir / f"{base_filename}.csv"
            df.to_csv(output_path, index=False)
        elif format == "parquet":
            output_path = self.output_dir / f"{base_filename}.parquet"
            df.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"  Saved {len(df)} records to {output_path}")
        return output_path
    
    def run_full_pipeline(self, sources: List[str], keyword: str = "artificial intelligence", 
                         output_format: str = "json") -> Dict[str, Path]:
        """Run complete ETL pipeline for specified sources."""
        print("=" * 60)
        print("Funding Data ETL Pipeline")
        print("=" * 60)
        print(f"Sources: {', '.join(sources)}")
        print(f"Keyword: {keyword}")
        print(f"Output format: {output_format}")
        print()
        
        output_files = {}
        
        for source in sources:
            try:
                # Extract
                if source.lower() == "sbir":
                    raw_data = self.extract_sbir(keyword)
                elif source.lower() == "nsf":
                    raw_data = self.extract_nsf(keyword)
                elif source.lower() == "nih":
                    raw_data = self.extract_nih(keyword)
                elif source.lower() == "diu":
                    raw_data = self.extract_diu()
                else:
                    print(f"  Unknown source: {source}, skipping...")
                    continue
                
                if not raw_data:
                    print(f"  No data extracted from {source}")
                    continue
                
                # Transform
                df = self.transform_funding_data(raw_data, source)
                
                # Load
                output_path = self.load_funding_data(df, source, output_format)
                output_files[source] = output_path
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"  Error processing {source}: {e}")
                continue
        
        # Create combined dataset
        self._create_combined_dataset(output_files, output_format)
        
        print()
        print("ETL pipeline complete!")
        return output_files
    
    def _create_combined_dataset(self, output_files: Dict[str, Path], output_format: str):
        """Combine all sources into a single dataset."""
        print("Creating combined dataset...")
        
        all_dfs = []
        for source, filepath in output_files.items():
            if filepath.suffix == ".json":
                df = pd.read_json(filepath)
            elif filepath.suffix == ".csv":
                df = pd.read_csv(filepath)
            elif filepath.suffix == ".parquet":
                df = pd.read_parquet(filepath)
            else:
                continue
            all_dfs.append(df)
        
        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            timestamp = datetime.now().strftime("%Y%m%d")
            combined_path = self.output_dir / f"combined_funding_{timestamp}.{output_format}"
            
            if output_format == "json":
                combined_df.to_json(combined_path, orient="records", indent=2, date_format="iso")
            elif output_format == "csv":
                combined_df.to_csv(combined_path, index=False)
            elif output_format == "parquet":
                combined_df.to_parquet(combined_path, index=False)
            
            print(f"  Combined dataset saved: {combined_path} ({len(combined_df)} records)")

def main():
    parser = argparse.ArgumentParser(description="ETL pipeline for U.S. AI funding data")
    parser.add_argument("--sources", nargs="+", 
                       choices=["sbir", "nsf", "nih", "diu", "all"],
                       default=["sbir"],
                       help="Data sources to extract")
    parser.add_argument("--keyword", default="artificial intelligence",
                       help="Search keyword")
    parser.add_argument("--format", choices=["json", "csv", "parquet"],
                       default="json",
                       help="Output format")
    
    args = parser.parse_args()
    
    if "all" in args.sources:
        sources = ["sbir", "nsf", "nih", "diu"]
    else:
        sources = args.sources
    
    etl = FundingETL()
    etl.run_full_pipeline(sources, args.keyword, args.format)

if __name__ == "__main__":
    main()

