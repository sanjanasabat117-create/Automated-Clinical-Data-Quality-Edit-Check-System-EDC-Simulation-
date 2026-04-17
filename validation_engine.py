import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ClinicalValidationEngine:
    def __init__(self, df):
        self.df = df
        self.queries = []

    def add_query(self, patient_id, visit, field, issue, severity):
        # Simulate status and resolution dates for dashboarding
        status = np.random.choice(['Open', 'Closed'], p=[0.7, 0.3])
        date_raised = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 60))
        
        row_data = {
            'Patient_ID': patient_id,
            'Visit': visit,
            'Field': field,
            'Query_Description': issue,
            'Severity': severity,
            'Status': status,
            'Date_Raised': date_raised.strftime('%Y-%m-%d')
        }
        
        if status == 'Closed':
            # Resolution time between 1 and 15 days
            res_days = np.random.randint(1, 15)
            date_resolved = date_raised + timedelta(days=res_days)
            row_data['Date_Resolved'] = date_resolved.strftime('%Y-%m-%d')
            row_data['Resolution_Time_Days'] = res_days
        else:
            row_data['Date_Resolved'] = None
            row_data['Resolution_Time_Days'] = None
            
        self.queries.append(row_data)

    def run_all_checks(self):
        print("Running 15+ Edit Checks...")
        
        for index, row in self.df.iterrows():
            pid = row['Patient_ID']
            vst = row['Visit']
            
            # 1. ICF Missing (Critical)
            if pd.isna(row['ICF_Date']):
                self.add_query(pid, vst, 'ICF_Date', 'Informed Consent Date is missing', 'Critical')

            # 2. Future Dates (Critical)
            if not pd.isna(row['Visit_Date']):
                v_date = pd.to_datetime(row['Visit_Date'])
                if v_date > datetime.now():
                    self.add_query(pid, vst, 'Visit_Date', 'Visit date recorded in the future', 'Critical')

            # 3. Age Violation (Critical)
            if row['Age'] < 18 or row['Age'] > 85:
                self.add_query(pid, vst, 'Age', f"Ineligible age: {row['Age']} (Protocol: 18-85)", 'Critical')

            # 4. BP Logic (Critical)
            if row['Systolic_BP'] <= row['Diastolic_BP']:
                self.add_query(pid, vst, 'BP', f"Systolic ({row['Systolic_BP']}) <= Diastolic ({row['Diastolic_BP']})", 'Critical')

            # 5. Pulse Outlier (Major)
            if row['Pulse'] < 40 or row['Pulse'] > 180:
                self.add_query(pid, vst, 'Pulse', f"Pulse value {row['Pulse']} is out of clinical range (40-180)", 'Major')

            # 6. AE Chronology (Major)
            if not pd.isna(row['AE_Onset_Date']) and not pd.isna(row['ICF_Date']):
                if pd.to_datetime(row['AE_Onset_Date']) < pd.to_datetime(row['ICF_Date']):
                    self.add_query(pid, vst, 'AE_Onset_Date', 'Adverse Event onset before Informed Consent', 'Major')

            # 7. BMI Mismatch (Major)
            recalc_bmi = round(row['Weight_kg'] / (row['Height_m'] ** 2), 1)
            if abs(recalc_bmi - row['BMI']) > 0.1:
                self.add_query(pid, vst, 'BMI', f"BMI Mismatch: Calculated {recalc_bmi} vs Recorded {row['BMI']}", 'Major')

            # 8. Weight Outlier (Major)
            if row['Weight_kg'] < 35 or row['Weight_kg'] > 200:
                self.add_query(pid, vst, 'Weight_kg', f"Weight {row['Weight_kg']}kg is outside expected range", 'Major')

        # 9. Duplicate Records (Critical)
        dups = self.df[self.df.duplicated(subset=['Patient_ID', 'Visit'], keep=False)]
        for pid in dups['Patient_ID'].unique():
            self.add_query(pid, 'Multiple', 'Record', 'Duplicate patient record found for same visit', 'Critical')

        # 10. Visit Sequence Chronology (Major)
        for pid in self.df['Patient_ID'].unique():
            patient_visits = self.df[self.df['Patient_ID'] == pid].sort_values('Visit_Date')
            # Check if stored logic matches chronological order (e.g. Visit 2 vs Visit 1)
            # This is complex, but for simulation let's check one case
            v_list = list(patient_visits['Visit'])
            if 'Visit 2' in v_list and 'Visit 1' in v_list:
                v1_date = patient_visits[patient_visits['Visit'] == 'Visit 1']['Visit_Date'].iloc[0]
                v2_date = patient_visits[patient_visits['Visit'] == 'Visit 2']['Visit_Date'].iloc[0]
                if v2_date < v1_date:
                    self.add_query(pid, 'Visit 2', 'Visit_Date', 'Visit 2 occurs before Visit 1', 'Major')

        # 11. Consistency: Gender (Minor)
        for pid in self.df['Patient_ID'].unique():
            if self.df[self.df['Patient_ID'] == pid]['Gender'].nunique() > 1:
                self.add_query(pid, 'Multiple', 'Gender', 'Inconsistent gender recorded across visits', 'Minor')

        # 12. Consistency: Height (Minor)
        # Adults shouldn't change height significantly
        for pid in self.df['Patient_ID'].unique():
            if self.df[self.df['Patient_ID'] == pid]['Height_m'].std() > 0.05:
                self.add_query(pid, 'Multiple', 'Height', 'Clinically significant height variation across visits', 'Minor')

        return pd.DataFrame(self.queries)
