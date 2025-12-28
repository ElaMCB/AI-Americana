#!/usr/bin/env bash
# Federal Register AI Documents Scraper
# Mirrors AI-related documents from the Federal Register
# Uses Federal Register API: https://www.federalregister.gov/api/v1/documents

set -e

# Configuration
OUTPUT_DIR="../policy/federal/fedreg"
API_BASE="https://www.federalregister.gov/api/v1/documents.json"
USER_AGENT="AI-Americana/1.0 (research project; contact: your-email@example.com)"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Search terms for AI-related documents
SEARCH_TERMS=(
    "artificial intelligence"
    "AI"
    "machine learning"
    "foundation model"
    "generative AI"
)

# Function to fetch documents from FedReg API
fetch_documents() {
    local search_term="$1"
    local page=1
    local per_page=1000
    local output_file="${OUTPUT_DIR}/fedreg_$(echo "$search_term" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')_$(date +%Y%m%d).json"
    
    echo "Fetching documents for: $search_term"
    
    # URL encode search term (basic encoding, for production use proper encoding)
    local encoded_term=$(echo "$search_term" | sed 's/ /%20/g')
    
    # Fetch documents
    curl -s -A "$USER_AGENT" \
        "${API_BASE}?q=${encoded_term}&per_page=${per_page}&page=${page}&order=newest" \
        -o "$output_file"
    
    # Check if we got results
    local count=$(jq -r '.count // 0' "$output_file" 2>/dev/null || echo "0")
    
    if [ "$count" -gt 0 ]; then
        echo "  Found $count documents, saved to $output_file"
        
        # Extract individual documents as separate markdown files
        extract_documents "$output_file"
    else
        echo "  No documents found"
        rm -f "$output_file"
    fi
    
    # Be respectful with rate limiting
    sleep 2
}

# Function to extract individual documents and save as markdown
extract_documents() {
    local json_file="$1"
    local base_dir="${OUTPUT_DIR}/documents"
    mkdir -p "$base_dir"
    
    # Use jq to extract and format each document
    if command -v jq >/dev/null 2>&1; then
        jq -r '.results[] | @json' "$json_file" | while IFS= read -r doc; do
            local doc_id=$(echo "$doc" | jq -r '.document_number')
            local title=$(echo "$doc" | jq -r '.title')
            local agency=$(echo "$doc" | jq -r '.agencies[0].name // "Unknown"')
            local pub_date=$(echo "$doc" | jq -r '.publication_date')
            local url=$(echo "$doc" | jq -r '.html_url')
            
            local md_file="${base_dir}/${doc_id}.md"
            
            cat > "$md_file" <<EOF
# $title

**Document Number:** $doc_id  
**Agency:** $agency  
**Publication Date:** $pub_date  
**Source URL:** $url

## Full Text

<!-- Full text would be fetched separately if needed -->
<!-- Use: curl "${url}.json" to get full document text -->

## Metadata

\`\`\`json
$doc
\`\`\`

EOF
            echo "  Extracted: $doc_id - $title"
        done
    else
        echo "  Warning: jq not installed, skipping individual document extraction"
        echo "  Install jq for better document parsing: https://stedolan.github.io/jq/"
    fi
}

# Function to fetch specific document types
fetch_by_type() {
    local doc_type="$1"  # e.g., "PRESDOCU" for Presidential Documents
    local output_file="${OUTPUT_DIR}/fedreg_${doc_type}_$(date +%Y%m%d).json"
    
    echo "Fetching documents of type: $doc_type"
    
    curl -s -A "$USER_AGENT" \
        "${API_BASE}?type=${doc_type}&per_page=1000&order=newest" \
        -o "$output_file"
    
    local count=$(jq -r '.count // 0' "$output_file" 2>/dev/null || echo "0")
    echo "  Found $count ${doc_type} documents"
    
    sleep 2
}

# Main execution
main() {
    echo "Federal Register AI Documents Scraper"
    echo "======================================"
    echo "Output directory: $OUTPUT_DIR"
    echo ""
    
    # Check for required tools
    if ! command -v curl >/dev/null 2>&1; then
        echo "Error: curl is required but not installed"
        exit 1
    fi
    
    # Fetch documents for each search term
    for term in "${SEARCH_TERMS[@]}"; do
        fetch_documents "$term"
    done
    
    # Also fetch presidential documents (often contain AI executive orders)
    fetch_by_type "PRESDOCU"
    
    # Create index file
    create_index
    
    echo ""
    echo "Scraping complete! Check $OUTPUT_DIR for results"
}

# Create index of all scraped documents
create_index() {
    local index_file="${OUTPUT_DIR}/index.md"
    
    cat > "$index_file" <<EOF
# Federal Register AI Documents Index

Generated: $(date -Iseconds)

## Search Results

EOF
    
    # List all JSON files
    for json_file in "${OUTPUT_DIR}"/fedreg_*.json; do
        if [ -f "$json_file" ]; then
            local basename=$(basename "$json_file")
            echo "- [$basename]($basename)" >> "$index_file"
        fi
    done
    
    echo "" >> "$index_file"
    echo "## Individual Documents" >> "$index_file"
    echo "" >> "$index_file"
    echo "See \`documents/\` directory for individual markdown files." >> "$index_file"
}

# Run main function
main

