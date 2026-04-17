import pandas as pd
from data_simulation import generate_dirty_data
from validation_engine import ClinicalValidationEngine
import os

def run_project():
    print("=== Clinical Data Quality & EDC Simulation ===")
    
    # 1. Check if raw data exists, else generate
    raw_data_path = "Clinical_Data_Quality_Project/raw_clinical_data.csv"
    if not os.path.exists(raw_data_path):
        raw_df = generate_dirty_data(200)
        raw_df.to_csv(raw_data_path, index=False)
    else:
        raw_df = pd.read_csv(raw_data_path)
    
    print(f"Loaded {len(raw_df)} records for validation.")

    # 2. Run Validation Engine
    engine = ClinicalValidationEngine(raw_df)
    query_log = engine.run_all_checks()

    # 3. Export Query Log
    output_path = "Clinical_Data_Quality_Project/edc_query_log.csv"
    query_log.to_csv(output_path, index=False)
    
    # 4. Impact Summary
    print("\n--- Validation Summary ---")
    print(f"Total Queries Raised: {len(query_log)}")
    print("\nQueries by Severity:")
    print(query_log['Severity'].value_counts())
    
    print(f"\nQuery Log exported to: {output_path}")
    print("==========================================")

if __name__ == "__main__":
    run_project()
