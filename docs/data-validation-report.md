# Data Validation Report

## 1. Purpose

This document records the data validation activities performed on the raw Telco Customer Churn dataset before preprocessing and model development.

The purpose of validation is to identify structural, datatype, missing-value, and data-quality issues without modifying the original raw dataset.

---

# 2. Dataset

**Dataset:** Telco Customer Churn

**Rows:** 7,043

**Columns:** 21

**Target:** `Churn`

**Dataset Location:**

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

The raw dataset is treated as read-only during the validation stage.

---

# 3. Validation Status

| Validation                       | Status                    |
| -------------------------------- | ------------------------- |
| Schema Validation                | ✅ Passed                  |
| Data Type Validation             | ⚠️ Investigation Required |
| Missing Value Validation         | ✅ Passed                  |
| Empty/Whitespace Validation      | ⚠️ Issue Identified       |
| Numerical Validation             | ⏳ Pending                 |
| Categorical Validation           | ⏳ Pending                 |
| Duplicate Row Validation         | ⏳ Pending                 |
| Duplicate Customer ID Validation | ⏳ Pending                 |
| Target Integrity Validation      | ⏳ Pending                 |
| Final Data Quality Report        | ⏳ Pending                 |

---

# 4. Schema Validation

The dataset was checked against the expected 21-column schema.

The following were validated:

* Expected columns are present.
* No unexpected columns were found.
* Column ordering matches the expected schema.

### Result

```text
Schema validation: PASSED
```

All expected columns are present.

---

# 5. Data Type Validation

The dataset was inspected to determine whether columns are represented using appropriate data types.

### Expected numerical columns

* `SeniorCitizen`
* `tenure`
* `MonthlyCharges`
* `TotalCharges`

### Expected string/categorical columns

* `customerID`
* `gender`
* `Partner`
* `Dependents`
* `PhoneService`
* `MultipleLines`
* `InternetService`
* `OnlineSecurity`
* `OnlineBackup`
* `DeviceProtection`
* `TechSupport`
* `StreamingTV`
* `StreamingMovies`
* `Contract`
* `PaperlessBilling`
* `PaymentMethod`
* `Churn`

### Observation

The current pandas environment represents string columns using the `str` dtype.

This is an acceptable representation for the string-based columns.

However:

```text
TotalCharges
Expected: numeric
Actual:   str
```

This requires further investigation because `TotalCharges` represents a monetary quantity.

### Result

```text
Data type validation: INVESTIGATION REQUIRED
```

The `TotalCharges` datatype will be investigated further during numerical validation and preprocessing.

---

# 6. Missing Value Validation

The dataset was checked for standard pandas missing values such as:

* `NaN`
* `None`
* `pd.NA`

All 7,043 records contain non-null values according to the validation.

### Result

```text
Missing value validation: PASSED
```

No standard pandas missing values were detected.

---

# 7. Empty and Whitespace Value Validation

String-based columns were additionally checked for:

* Empty strings
* Whitespace-only strings

This validation identified:

```text
TotalCharges: 11 empty/whitespace values
```

No other columns were reported with empty or whitespace-only values.

---

# 8. TotalCharges Investigation

The 11 empty `TotalCharges` records were inspected to determine whether they represent random data corruption or a meaningful business/data condition.

The affected records are:

| Customer ID | Tenure | Monthly Charges | Total Charges | Churn |
| ----------- | -----: | --------------: | ------------- | ----- |
| 4472-LVYGI  |      0 |           52.55 | Empty         | No    |
| 3115-CZMZD  |      0 |           20.25 | Empty         | No    |
| 5709-LVOEQ  |      0 |           80.85 | Empty         | No    |
| 4367-NUYAO  |      0 |           25.75 | Empty         | No    |
| 1371-DWPAZ  |      0 |           56.05 | Empty         | No    |
| 7644-OMVMY  |      0 |           19.85 | Empty         | No    |
| 3213-VVOLG  |      0 |           25.35 | Empty         | No    |
| 2520-SGTTA  |      0 |           20.00 | Empty         | No    |
| 2923-ARZLG  |      0 |           19.70 | Empty         | No    |
| 4075-WKNIU  |      0 |           73.35 | Empty         | No    |
| 2775-SEFEE  |      0 |           61.90 | Empty         | No    |

---

# 9. 4.4 Conclusion — Empty/Whitespace Validation

The empty-value investigation produced an important finding.

There are **11 empty `TotalCharges` values** in the dataset.

All 11 affected customers have:

```text
tenure = 0
```

and:

```text
Churn = No
```

The affected customers also have valid `MonthlyCharges` values.

This suggests that the empty `TotalCharges` values are not necessarily arbitrary corrupted records. They appear to correspond to customers with zero-month tenure, for whom accumulated total charges may not yet have been recorded.

However, this is currently a **data-quality hypothesis**, not a final preprocessing decision.

Therefore:

* The raw values will **not** be manually modified.
* The empty values will **not** be replaced with zero during validation.
* The `TotalCharges` column will remain unchanged in the raw dataset.
* The issue will be handled explicitly during the preprocessing/data-transformation stage after numerical validation is complete.

### Final finding

```text
11 empty/whitespace values found in TotalCharges.

All 11 records have tenure = 0.

The values appear to have a plausible business explanation
and require controlled handling during preprocessing.
```

---

# 10. Engineering Decision

The raw dataset must remain unchanged.

The validation layer is responsible only for:

1. Detecting data-quality issues.
2. Reporting those issues.
3. Providing evidence for later transformation decisions.

Data transformation will be performed in a separate preprocessing stage.

This separation ensures that:

```text
Raw Dataset
     ↓
Validation
     ↓
Data Quality Findings
     ↓
Preprocessing Decisions
     ↓
Processed Dataset
```

rather than modifying the source data during validation.

---

# 11. Automated Tests

The validation functionality is covered by automated pytest tests.

Current test suite:

```text
8 passed
```

The tests currently cover:

* Dataset loading
* Expected columns
* Missing-file handling
* Project setup
* Schema validation
* Data type validation
* Missing-value validation
* Empty/whitespace validation

---

# 12. Next Validation Steps

The remaining Stage 04 validation activities are:

### 4.5 Numerical Validation

Validate:

* `SeniorCitizen`
* `tenure`
* `MonthlyCharges`
* `TotalCharges`

Including:

* Valid ranges
* Negative values
* Impossible values
* Numeric conversion feasibility
* Numerical anomalies

### 4.6 Categorical Validation

Validate:

* Allowed categorical values
* Unexpected categories
* Spelling inconsistencies
* Unexpected whitespace
* Target categories

### 4.7 Duplicate Row Validation

Determine whether complete duplicate records exist.

### 4.8 Duplicate Customer ID Validation

Determine whether `customerID` is truly unique.

### 4.9 Target Integrity Validation

Validate that `Churn` contains only the expected target classes:

```text
Yes
No
```

### 4.10 Final Data Quality Report

Combine all validation findings into a final quality assessment before preprocessing begins.

---

# 13. Stage 04 Exit Criteria

Stage 04 will be considered complete when:

* [ ] Schema is validated.
* [ ] Data types are validated.
* [ ] Missing values are investigated.
* [ ] Empty/whitespace values are investigated.
* [ ] Numerical values are validated.
* [ ] Categorical values are validated.
* [ ] Duplicate rows are checked.
* [ ] Customer ID uniqueness is checked.
* [ ] Target integrity is validated.
* [ ] All findings are documented.
* [ ] Automated tests cover the validation logic.
* [ ] A final data-quality decision is documented.

Only after these criteria are satisfied will the project proceed to preprocessing.
