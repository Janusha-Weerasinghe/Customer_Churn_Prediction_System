# Data Validation Report

## 1. Purpose

This document records the data validation activities performed on the raw Telco Customer Churn dataset before preprocessing and model development.

The purpose of validation is to identify structural, datatype, missing-value, numerical, categorical, duplication, target-integrity, and other data-quality issues without modifying the original raw dataset.

The validation stage establishes data-quality evidence and engineering decisions before the dataset enters the preprocessing and machine learning pipeline.

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

No records or values are modified during validation.

---

# 3. Validation Status

| Validation                       | Status                    |
| -------------------------------- | ------------------------- |
| Schema Validation                | ✅ Passed                  |
| Data Type Validation             | ⚠️ Investigation Required |
| Missing Value Validation         | ✅ Passed                  |
| Empty/Whitespace Validation      | ⚠️ Issue Identified       |
| Numerical Validation             | ✅ Passed                  |
| Categorical Validation           | ✅ Passed                  |
| Duplicate Row Validation         | ✅ Passed                  |
| Duplicate Customer ID Validation | ✅ Passed                  |
| Target Integrity Validation      | ✅ Passed                  |
| Final Data Quality Assessment    | ✅ Completed               |

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

All expected columns are present and the dataset structure matches the expected schema.

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

The issue was investigated further through empty-value and numerical validation.

### Result

```text
Data type validation: INVESTIGATION REQUIRED
```

The `TotalCharges` datatype will be converted to an appropriate numerical representation during the preprocessing stage.

The raw dataset will remain unchanged.

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

### Result

```text
Empty/whitespace validation: INVESTIGATION REQUIRED
```

The identified values were investigated in the following section.

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

# 9. Empty/Whitespace Validation Conclusion

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

However, this remains a **data-quality hypothesis**, not a definitive business interpretation.

Therefore:

* The raw values will **not** be manually modified.
* The empty values will **not** be replaced with zero during validation.
* The `TotalCharges` column will remain unchanged in the raw dataset.
* The issue will be handled explicitly during the preprocessing/data-transformation stage.

### Final finding

```text
11 empty/whitespace values found in TotalCharges.

All 11 records have tenure = 0.

The values appear to have a plausible business explanation
and require controlled handling during preprocessing.
```

---

# 10. Numerical Validation

The numerical columns were validated against expected data-quality and business rules.

### `SeniorCitizen`

The column was checked to ensure that values are restricted to:

```text
0
1
```

No invalid values were detected.

### `tenure`

The column was checked to ensure that values are not negative.

No negative values were detected.

### `MonthlyCharges`

The column was checked to ensure that:

* It is numerically represented.
* Values are not negative.

No invalid values were detected.

### `TotalCharges`

Non-empty values were checked for numerical convertibility.

The non-empty values were successfully interpreted as numerical values.

The 11 empty/whitespace values were already identified separately and will be handled during preprocessing.

### Result

```text
Numerical validation: PASSED
```

No violations of the defined numerical business rules were detected.

---

# 11. Categorical Validation

Categorical columns were validated against their expected domain values.

The following columns were checked:

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

The validation checked for unexpected categorical values and domain inconsistencies.

### Result

```text
Categorical validation: PASSED
```

No unexpected categorical values were detected.

---

# 12. Duplicate Row Validation

The dataset was checked for exact duplicate rows.

An exact duplicate row is a record where all column values match another record in the dataset.

### Result

```text
Duplicate row validation: PASSED
```

No exact duplicate rows were detected.

---

# 13. Duplicate Customer ID Validation

The `customerID` column was checked to determine whether each customer identifier is unique.

Customer IDs are expected to uniquely identify individual customer records.

### Result

```text
Duplicate customer ID validation: PASSED
```

No duplicate customer IDs were detected.

The `customerID` field therefore satisfies the expected uniqueness constraint.

---

# 14. Target Integrity Validation

The target variable for this project is:

```text
Churn
```

The expected target classes are:

```text
Yes
No
```

The target variable was validated for:

* Missing values
* Empty/whitespace values
* Unexpected target values
* Presence of both target classes

### Result

```text
Target integrity validation: PASSED
```

The `Churn` target contains valid `Yes` and `No` classes with no target-integrity violations detected.

---

# 15. Engineering Decision

The raw dataset must remain unchanged.

The validation layer is responsible only for:

1. Detecting data-quality issues.
2. Reporting those issues.
3. Investigating potential causes.
4. Providing evidence for later transformation decisions.

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

# 16. Final Data Quality Assessment

The raw dataset is considered **structurally suitable for proceeding to preprocessing**.

The following validation checks passed successfully:

* Schema validation
* Missing-value validation
* Numerical validation
* Categorical validation
* Duplicate-row validation
* Duplicate customer ID validation
* Target integrity validation

Two data-quality findings require controlled handling during preprocessing:

### Finding 1 — `TotalCharges` data type

`TotalCharges` is stored as a string in the raw dataset even though it represents a numerical monetary value.

**Decision:**

Convert the column to a numerical representation during preprocessing.

### Finding 2 — Empty `TotalCharges` values

There are 11 empty/whitespace `TotalCharges` values.

All 11 records have:

```text
tenure = 0
Churn = No
```

**Decision:**

Do not manually modify the raw dataset.

Handle the values explicitly within the preprocessing pipeline after converting `TotalCharges` to numeric.

---

# 17. Automated Validation Tests

The validation functionality is covered by automated `pytest` tests.

The current validation test suite covers:

* Dataset loading
* Missing-file handling
* Project setup
* Schema validation
* Data type validation
* Missing-value validation
* Empty/whitespace validation
* Numerical validation
* Categorical validation
* Duplicate-row validation
* Duplicate customer ID validation
* Target integrity validation

The expected final test result is:

```text
13 passed
```

All validation logic is therefore protected by automated tests.

---

# 18. Validation Limitations

The validation stage intentionally does not perform the following operations:

* Missing-value imputation
* Data type transformation
* Feature engineering
* Outlier removal
* Categorical encoding
* Feature scaling
* Target encoding
* Duplicate removal
* Model training

These operations belong to later stages of the machine learning pipeline.

This ensures a clear separation between:

```text
Validation
```

and:

```text
Preprocessing / Transformation
```

---

# 19. Stage 04 Conclusion

## Stage 04 — Data Validation: COMPLETE

The raw Telco Customer Churn dataset has been systematically validated without modifying the original data.

The dataset passed the major structural, numerical, categorical, duplication, and target-integrity checks.

The identified `TotalCharges` issues have been documented and will be handled in the preprocessing pipeline.

### Final Validation Decision

```text
Dataset Status: READY FOR PREPROCESSING
Raw Dataset: PRESERVED
Validation: COMPLETE
Known Issues: DOCUMENTED
Automated Tests: PASSING
```

The project can now proceed to the next stage.

---

# 20. Next Stage

## Stage 05 — Exploratory Data Analysis (EDA)

The next stage will investigate the underlying patterns and relationships in the dataset before model development.

The EDA will cover:

* Target distribution
* Numerical feature distributions
* Categorical feature distributions
* Churn rate by feature
* Customer tenure patterns
* Monthly and total charge patterns
* Contract-related churn behavior
* Payment-method patterns
* Service adoption patterns
* Correlation analysis
* Potential outliers
* Potential feature relationships
* Business-oriented churn insights

The objective is to understand **why customers may be churning** and identify useful patterns that can guide preprocessing, feature engineering, model selection, and evaluation.
