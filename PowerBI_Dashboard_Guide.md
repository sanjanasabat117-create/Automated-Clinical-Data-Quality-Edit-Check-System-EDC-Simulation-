# Power BI Dashboard Implementation Guide: Clinical Data Quality

This guide provides the technical logic (Power Query and DAX) required to build the **Clinical Data Quality & Query Management Dashboard** mentioned in your portfolio.

## 1. Data Ingestion (Power Query / M)

After importing `edc_query_log.csv` into Power BI, apply the following transformations in the **Power Query Editor**:

1.  **Date Conversion:** Ensure `Date_Raised` and `Date_Resolved` are set to **Date** data type.
2.  **Replace Table Name:** Rename the table to `QueryLog`.
3.  **Add Aging Column (Optional):**
    ```m
    // Custom Column: Query_Age
    if [Status] = "Open" then Duration.Days(DateTime.Date(DateTime.LocalNow()) - [Date_Raised]) else null
    ```

---

## 2. Calculated Measures (DAX)

Create the following measures to track site performance and resolution metrics.

### A. Core Metrics
```dax
Total Queries = COUNT(QueryLog[Patient_ID])

Open Queries = CALCULATE([Total Queries], QueryLog[Status] = "Open")

Closed Queries = CALCULATE([Total Queries], QueryLog[Status] = "Closed")

Open Query Rate % = DIVIDE([Open Queries], [Total Queries], 0)
```

### B. Resolution Timeline
```dax
Avg. Resolution Days = AVERAGE(QueryLog[Resolution_Time_Days])

Critical Open Queries = 
CALCULATE(
    [Open Queries], 
    QueryLog[Severity] = "Critical"
)
```

### C. Site-wise Data Quality Score (The "Algorithm")
This measure creates a weighted score from 0-100 for each site. Sites lose more points for Critical/Major errors.

```dax
Site Quality Score = 
VAR Penalty = 
    CALCULATE(COUNT(QueryLog[Patient_ID]), QueryLog[Severity] = "Critical") * 10 +
    CALCULATE(COUNT(QueryLog[Patient_ID]), QueryLog[Severity] = "Major") * 4 +
    CALCULATE(COUNT(QueryLog[Patient_ID]), QueryLog[Severity] = "Minor") * 1
VAR BaseScore = 100
VAR TotalRecords = CALCULATE(COUNT(QueryLog[Patient_ID]), ALLSELECTED(QueryLog))
VAR FinalScore = BaseScore - (Penalty / TotalRecords * 10)
RETURN
IF(FinalScore < 0, 0, FinalScore)
```

---

## 3. Recommended Visualizations

To showcase this on your portfolio, build the following pages:

### Page 1: Executive Overview
*   **Card Visuals:** [Open Query Rate %], [Avg. Resolution Days], [Critical Open Queries].
*   **Clustered Column Chart:** Queries by `Severity` (Critical vs Major vs Minor).
*   **Donut Chart:** Status Breakdown (Open vs Closed).

### Page 2: Site Performance
*   **Table/Matrix:** Rows: `Site_ID` | Columns: [Site Quality Score], [Total Queries], [Avg. Resolution Days].
*   **Scatter Chart:** X-Axis: [Total Queries] | Y-Axis: [Avg. Resolution Days] | Size: [Critical Open Queries]. This highlights sites with high volume and slow response.

---

## 4. Key Talking Points for Interviews
*   **Logic-Driven Quality:** "I developed a weighted scoring algorithm that penalizes sites more heavily for safety-critical errors (Critical/Major) compared to minor documentation issues."
*   **Operational Visibility:** "The dashboard provides real-time visibility into Query Aging, allowing Clinical Research Associates (CRAs) to prioritize their site monitoring visits."
*   **ICH-GCP Compliance:** "The system ensures data integrity by tracking every discrepancy from discovery to resolution, maintaining a clear audit trail."
