import os
import json

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'raw')
EXPECTED_FILES = ['cms_enrollment_raw.json', 'reddit_sentiment_raw.json']

def run_tests():
    print("=========================================")
    print("[TEST] Running Data Lake Validation Tests [TEST]")
    print("=========================================\n")
    
    if not os.path.exists(RAW_DATA_DIR):
        print("[FAIL] Raw data directory does not exist.")
        return

    for filename in EXPECTED_FILES:
        file_path = os.path.join(RAW_DATA_DIR, filename)
        
        # Test 1: File Exists
        if not os.path.exists(file_path):
            print(f"[FAIL] {filename} is missing.")
            continue
        print(f"[PASS] {filename} exists.")
        
        # Test 2: File is valid JSON and not empty
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Test 3: Check schema (metadata and records exist)
            if "metadata" not in data or "records" not in data:
                print(f"[FAIL] {filename} is missing required 'metadata' or 'records' keys.")
                continue
                
            record_count = data['metadata']['record_count']
            if record_count == 0:
                print(f"[WARNING] {filename} is valid JSON but contains 0 records.")
            else:
                print(f"[PASS] {filename} parsed successfully. Contains {record_count} records.")
                
            # Preview the first record
            print(f"   -> First record sample keys: {list(data['records'][0].keys())}")
            
        except json.JSONDecodeError:
            print(f"[FAIL] {filename} contains invalid JSON.")
            
    print("\n=========================================")
    print("Validation Complete.")
    print("=========================================")

if __name__ == "__main__":
    run_tests()