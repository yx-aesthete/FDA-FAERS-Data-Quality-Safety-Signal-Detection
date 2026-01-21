"""
Automatic FAERS data downloader for deployment
Downloads and extracts FAERS Q3 2025 data if not present
"""

import os
import urllib.request
import zipfile
from pathlib import Path


def download_and_extract_faers_data():
    """Download and extract FAERS Q3 2025 data if not already present"""
    
    data_path = Path(__file__).parent / 'data'
    ascii_path = data_path / 'ASCII'
    demo_file = ascii_path / 'DEMO25Q3.txt'
    
    # Check if data already exists
    if demo_file.exists():
        print("✅ FAERS data already available")
        return True
    
    print("📥 Downloading FAERS Q3 2025 data (73MB)...")
    
    # Create directories
    data_path.mkdir(exist_ok=True)
    ascii_path.mkdir(exist_ok=True)
    
    # Download URL
    url = 'https://fis.fda.gov/content/Exports/faers_ascii_2025q3.zip'
    zip_path = data_path / 'faers_ascii_2025q3.zip'
    
    try:
        # Download with progress
        urllib.request.urlretrieve(url, zip_path)
        print("✅ Download complete")
        
        # Extract
        print("📦 Extracting data files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_path)
        print("✅ Extraction complete")
        
        # Verify key files exist
        required_files = ['DEMO25Q3.txt', 'REAC25Q3.txt', 'DRUG25Q3.txt', 'OUTC25Q3.txt']
        for file in required_files:
            if not (ascii_path / file).exists():
                print(f"⚠️ Warning: {file} not found")
                return False
        
        print("✅ All data files ready")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading data: {e}")
        print("\n⚠️ Please download manually from:")
        print("https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html")
        return False


if __name__ == "__main__":
    download_and_extract_faers_data()
