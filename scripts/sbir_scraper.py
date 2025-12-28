#!/usr/bin/env python3
"""
SBIR Awards Scraper
Scrapes SBIR awards matching keyword "artificial intelligence" and saves to JSON.
Data source: SBIR.gov API and/or web scraping
"""

import json
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "funding"
OUTPUT_DIR.mkdir(exist_ok=True)
SBIR_API_BASE = "https://www.sbir.gov/api/awards.json"
SBIR_WEB_BASE = "https://www.sbir.gov/sbc/awards"

def fetch_sbir_api(keyword: str = "artificial intelligence", limit: int = 1000) -> List[Dict]:
    """
    Fetch SBIR awards from API matching keyword.
    
    Note: SBIR.gov may have rate limits. Check their API documentation
    for the actual endpoint structure and parameters.
    """
    awards = []
    
    try:
        # Example API call structure (adjust based on actual SBIR.gov API)
        params = {
            "keyword": keyword,
            "limit": limit,
            "format": "json"
        }
        
        response = requests.get(SBIR_API_BASE, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        # Adjust parsing based on actual API response structure
        if isinstance(data, dict) and "awards" in data:
            awards = data["awards"]
        elif isinstance(data, list):
            awards = data
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        print("Note: You may need to use web scraping as fallback")
    
    return awards

def scrape_sbir_web(keyword: str = "artificial intelligence", max_pages: int = 10) -> List[Dict]:
    """
    Fallback: Scrape SBIR awards from web interface.
    
    This is a template - actual implementation depends on SBIR.gov HTML structure.
    You may need to use Selenium or Playwright for JavaScript-rendered content.
    """
    awards = []
    
    # TODO: Implement web scraping logic
    # - Navigate to SBIR.gov awards search
    # - Search for keyword
    # - Parse award listings
    # - Extract: title, company, award amount, date, agency, description
    
    print(f"Web scraping for '{keyword}' not yet implemented")
    print("Consider using: requests + BeautifulSoup or Selenium for dynamic content")
    
    return awards

def filter_ai_relevant(awards: List[Dict], keyword: str = "artificial intelligence") -> List[Dict]:
    """Filter awards to only those truly relevant to AI."""
    filtered = []
    keyword_lower = keyword.lower()
    ai_terms = ["artificial intelligence", "ai", "machine learning", "ml", 
                "neural network", "deep learning", "natural language processing"]
    
    for award in awards:
        # Check title, description, and abstract fields
        text_fields = " ".join([
            award.get("title", ""),
            award.get("abstract", ""),
            award.get("description", ""),
            award.get("summary", "")
        ]).lower()
        
        if any(term in text_fields for term in ai_terms):
            filtered.append(award)
    
    return filtered

def save_awards_json(awards: List[Dict], filename: Optional[str] = None) -> Path:
    """Save awards to JSON file with timestamp."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"sbir_awards_ai_{timestamp}.json"
    
    output_path = OUTPUT_DIR / filename
    
    output_data = {
        "metadata": {
            "source": "SBIR.gov",
            "scrape_date": datetime.now().isoformat(),
            "keyword": "artificial intelligence",
            "count": len(awards)
        },
        "awards": awards
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(awards)} awards to {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Scrape SBIR awards for AI-related projects")
    parser.add_argument("--keyword", default="artificial intelligence",
                       help="Search keyword (default: 'artificial intelligence')")
    parser.add_argument("--limit", type=int, default=1000,
                       help="Maximum number of awards to fetch")
    parser.add_argument("--method", choices=["api", "web", "both"], default="api",
                       help="Scraping method to use")
    parser.add_argument("--output", help="Output filename (default: auto-generated)")
    
    args = parser.parse_args()
    
    awards = []
    
    if args.method in ["api", "both"]:
        print(f"Fetching from SBIR API with keyword: '{args.keyword}'...")
        api_awards = fetch_sbir_api(args.keyword, args.limit)
        awards.extend(api_awards)
        time.sleep(1)  # Be respectful with rate limiting
    
    if args.method in ["web", "both"]:
        print(f"Scraping SBIR website with keyword: '{args.keyword}'...")
        web_awards = scrape_sbir_web(args.keyword)
        awards.extend(web_awards)
    
    # Filter for AI relevance
    filtered_awards = filter_ai_relevant(awards, args.keyword)
    
    # Save to JSON
    output_path = save_awards_json(filtered_awards, args.output)
    
    print(f"\nSummary:")
    print(f"  Total awards fetched: {len(awards)}")
    print(f"  AI-relevant awards: {len(filtered_awards)}")
    print(f"  Output file: {output_path}")

if __name__ == "__main__":
    main()

