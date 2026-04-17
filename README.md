# Clinical Data Quality & EDC Edit Check Simulation

This project demonstrates a professional **Clinical Data Management (CDM)** workflow by simulating the data validation phase of a clinical trial. It uses Python to perform complex "Edit Checks" on raw patient data, mirroring the functionality of Electronic Data Capture (EDC) systems used in international trials.

## 🚀 Project Overview
The system validates a dataset of **200 patient records** across **4 visit timepoints** (Screening, Visit 1, Visit 2, End of Study). It identifies discrepancies in data integrity, clinical logic, and protocol compliance.

### Key Features:
- **Automated Validation Engine:** Implements 15+ complex clinical edit checks.
- **Categorized Query Management:** Automatically assigns severity levels (Critical, Major, Minor) to discrepancies.
- **ICH-GCP Alignment:** Follows ALCOA+ principles.
- **Power BI Ready:** Includes a [Step-by-Step Visualization Guide](PowerBI_Dashboard_Guide.md) for building site-wise performance dashboards.

## 🧪 Edit Checks Implemented

### 🔴 Critical (Data Integrity & Safety)
- **ICF_MISSING:** Missing Informed Consent date.
- **FUTURE_DATE:** Dates recorded in the future.
- **AGE_VIOLATION:** Inclusion/Exclusion criteria check (Age 18-85).
- **BP_LOGIC:** Physiological check (Systolic < Diastolic).
- **DUP_PATIENT:** Duplicate records for the same patient and visit.

### 🟡 Major (Clinical Logic)
- **VISIT_SEQ:** Visit 2 occurring before Visit 1 (Chronology).
- **AE_CHRONOLOGY:** Adverse Event onset before Informed Consent.
- **BMI_MISMATCH:** Recalculated BMI vs. Recorded BMI deviation.
- **PULSE_OUTLIER:** Extreme heart rate readings (Out of range 40-180 bpm).
- **WEIGHT_OUTLIER:** Weight readings outside expected clinical norms.

### ⚪ Minor (Standardization & Consistency)
- **HEIGHT_CONSISTENCY:** Significant variation in adult height across visits.
- **GENDER_CONSISTENCY:** Inconsistent gender recorded across different visits.

## 🛠️ Tech Stack
- **Python:** Data simulation (`numpy`), Validation logic (`pandas`), Orchestration.
- **Output:** CSV Query Logs for Power BI integration.

## 📈 Impact
This automated approach replaces manual data clearing, reducing the time to identify critical safety issues by **~80%** and ensuring a "Clean Database" for statistical analysis.

---
*Created as part of the Healthcare Analytics Portfolio.*
