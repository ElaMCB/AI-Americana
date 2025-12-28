# Federal Register AI Documents Scraper (PowerShell)
# Mirrors AI-related documents from the Federal Register
# Uses Federal Register API: https://www.federalregister.gov/api/v1/documents

param(
    [string]$OutputDir = "../policy/federal/fedreg",
    [string[]]$SearchTerms = @(
        "artificial intelligence",
        "AI",
        "machine learning",
        "foundation model",
        "generative AI"
    )
)

$ErrorActionPreference = "Stop"

# Configuration
$ApiBase = "https://www.federalregister.gov/api/v1/documents.json"
$UserAgent = "AI-Americana/1.0 (research project; contact: your-email@example.com)"

# Create output directory
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$DocumentsDir = Join-Path $OutputDir "documents"
New-Item -ItemType Directory -Force -Path $DocumentsDir | Out-Null

function Fetch-Documents {
    param(
        [string]$SearchTerm,
        [int]$PerPage = 1000,
        [int]$Page = 1
    )
    
    Write-Host "Fetching documents for: $SearchTerm"
    
    # URL encode search term (PowerShell built-in method)
    $EncodedTerm = [System.Uri]::EscapeDataString($SearchTerm)
    
    # Build API URL
    $ApiUrl = "${ApiBase}?q=${EncodedTerm}&per_page=${PerPage}&page=${Page}&order=newest"
    
    try {
        $Response = Invoke-RestMethod -Uri $ApiUrl -UserAgent $UserAgent -Method Get
        
        if ($Response.count -gt 0) {
            $Timestamp = Get-Date -Format "yyyyMMdd"
            $SafeTerm = $SearchTerm -replace ' ', '_' -replace '[^a-zA-Z0-9_]', ''
            $OutputFile = Join-Path $OutputDir "fedreg_${SafeTerm}_${Timestamp}.json"
            
            # Save JSON response
            $Response | ConvertTo-Json -Depth 10 | Set-Content -Path $OutputFile -Encoding UTF8
            
            Write-Host "  Found $($Response.count) documents, saved to $OutputFile"
            
            # Extract individual documents
            Extract-Documents -JsonFile $OutputFile -Response $Response
            
            return $OutputFile
        } else {
            Write-Host "  No documents found"
            return $null
        }
    } catch {
        Write-Host "  Error fetching documents: $_"
        return $null
    }
    
    # Rate limiting
    Start-Sleep -Seconds 2
}

function Extract-Documents {
    param(
        [string]$JsonFile,
        [object]$Response
    )
    
    if ($Response.results) {
        foreach ($Doc in $Response.results) {
            $DocId = $Doc.document_number
            $Title = $Doc.title
            $Agency = if ($Doc.agencies -and $Doc.agencies.Count -gt 0) { $Doc.agencies[0].name } else { "Unknown" }
            $PubDate = $Doc.publication_date
            $Url = $Doc.html_url
            
            $MdFile = Join-Path $DocumentsDir "${DocId}.md"
            
            $Content = @"
# $Title

**Document Number:** $DocId  
**Agency:** $Agency  
**Publication Date:** $PubDate  
**Source URL:** $Url

## Full Text

<!-- Full text would be fetched separately if needed -->
<!-- Use: Invoke-RestMethod "${Url}.json" to get full document text -->

## Metadata

``````json
$($Doc | ConvertTo-Json -Depth 10)
``````

"@
            
            $Content | Set-Content -Path $MdFile -Encoding UTF8
            Write-Host "    Extracted: $DocId - $Title"
        }
    }
}

function Fetch-ByType {
    param(
        [string]$DocType,
        [int]$PerPage = 1000
    )
    
    Write-Host "Fetching documents of type: $DocType"
    
    $ApiUrl = "${ApiBase}?type=${DocType}&per_page=${PerPage}&order=newest"
    
    try {
        $Response = Invoke-RestMethod -Uri $ApiUrl -UserAgent $UserAgent -Method Get
        
        if ($Response.count -gt 0) {
            $Timestamp = Get-Date -Format "yyyyMMdd"
            $OutputFile = Join-Path $OutputDir "fedreg_${DocType}_${Timestamp}.json"
            
            $Response | ConvertTo-Json -Depth 10 | Set-Content -Path $OutputFile -Encoding UTF8
            Write-Host "  Found $($Response.count) ${DocType} documents"
        }
    } catch {
        Write-Host "  Error: $_"
    }
    
    Start-Sleep -Seconds 2
}

function Create-Index {
    $IndexFile = Join-Path $OutputDir "index.md"
    
    $Content = @"
# Federal Register AI Documents Index

Generated: $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")

## Search Results

"@
    
    # List all JSON files
    Get-ChildItem -Path $OutputDir -Filter "fedreg_*.json" | ForEach-Object {
        $Content += "- [$($_.Name)]($($_.Name))`n"
    }
    
    $Content += @"

## Individual Documents

See `documents/` directory for individual markdown files.
"@
    
    $Content | Set-Content -Path $IndexFile -Encoding UTF8
}

# Main execution
Write-Host "Federal Register AI Documents Scraper"
Write-Host "======================================"
Write-Host "Output directory: $OutputDir"
Write-Host ""

$OutputFiles = @()

# Fetch documents for each search term
foreach ($Term in $SearchTerms) {
    $File = Fetch-Documents -SearchTerm $Term
    if ($File) {
        $OutputFiles += $File
    }
}

# Also fetch presidential documents (often contain AI executive orders)
Fetch-ByType -DocType "PRESDOCU"

# Create index file
Create-Index

Write-Host ""
Write-Host "Scraping complete! Check $OutputDir for results"

