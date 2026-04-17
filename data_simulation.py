import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dirty_data(num_patients=200):
    """
    Generates synthetic clinical trial data for 200 patients across 4 visits.
    Intentionally introduces errors to be caught by the Edit Check system.
    """
    print(f"Generating clinical data for {num_patients} patients...")
    np.random.seed(42)
    
    visit_names = ['Screening', 'Visit 1', 'Visit 2', 'End of Study']
    data_rows = []
    
    for p_id in range(1001, 1001 + num_patients):
        # Base demographics
        age = np.random.randint(20, 80, 1)[0]
        gender = np.random.choice(['M', 'F'], 1)[0]
        site_id = np.random.choice(['SITE_01', 'SITE_02', 'SITE_03', 'SITE_04'], 1)[0]
        
        # Informed Consent Date (ICF)
        icf_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 30))
        
        # Plant Error: Missing ICF for patient 1010
        if p_id == 1010:
            icf_date = None
        
        # Plant Error: Underage patient for 1005
        if p_id == 1005:
            age = 16
            
        current_date = icf_date if icf_date else datetime(2024, 1, 1)
        
        for i, visit in enumerate(visit_names):
            # Advance time for each visit (approx 30 days)
            current_date += timedelta(days=np.random.randint(25, 35))
            
            # Plant Error: Chronology error for patient 1025 (Visit 2 before Visit 1)
            visit_date = current_date
            if p_id == 1025 and visit == 'Visit 2':
                visit_date = data_rows[-1]['Visit_Date'] - timedelta(days=5)
            
            # Plant Error: Future date for patient 1060
            if p_id == 1060 and visit == 'End of Study':
                visit_date = datetime.now() + timedelta(days=365)
            
            # Vitals
            sys_bp = np.random.randint(110, 160)
            dia_bp = np.random.randint(70, 95)
            
            # Plant Error: Logic BP for patient 1040
            if p_id == 1040 and visit == 'Visit 1':
                sys_bp, dia_bp = 80, 120
            
            # Plant Error: Pulse Outlier for patient 1080
            pulse = np.random.randint(60, 100)
            if p_id == 1080 and visit == 'Screening':
                pulse = 220
            
            # BMI and Weight
            weight = np.random.uniform(50, 120)
            height = np.random.uniform(1.5, 2.0)
            bmi = round(weight / (height ** 2), 1)
            
            # Plant Error: BMI mismatch for patient 1100
            if p_id == 1100 and visit == 'Visit 1':
                bmi = 45.0 # Weight/Height won't match this
            
            # AE Chronology simulation
            ae_onset = None
            if np.random.random() < 0.1: # 10% chance of AE
                ae_onset = icf_date + timedelta(days=np.random.randint(-10, 50)) if icf_date else None
            
            # Plant Error: AE before ICF for patient 1120
            if p_id == 1120 and visit == 'Visit 1':
                ae_onset = icf_date - timedelta(days=10) if icf_date else None
            
            data_rows.append({
                'Patient_ID': p_id,
                'Site_ID': site_id,
                'Age': age,
                'Gender': gender,
                'Visit': visit,
                'Visit_Date': visit_date,
                'ICF_Date': icf_date,
                'Systolic_BP': sys_bp,
                'Diastolic_BP': dia_bp,
                'Pulse': pulse,
                'Weight_kg': round(weight, 1),
                'Height_m': round(height, 2),
                'BMI': bmi,
                'AE_Onset_Date': ae_onset
            })

    df = pd.DataFrame(data_rows)
    # Plant Error: Duplicate Record for 1150
    dup_row = df[df['Patient_ID'] == 1150].iloc[0].copy()
    df = pd.concat([df, pd.DataFrame([dup_row])], ignore_index=True)
    
    return df

if __name__ == "__main__":
    raw_dat = generate_dirty_data(200)
    raw_dat.to_csv("Clinical_Data_Quality_Project/raw_clinical_data.csv", index=False)
    print(f"Saved 200 patient records to raw_clinical_data.csv")
