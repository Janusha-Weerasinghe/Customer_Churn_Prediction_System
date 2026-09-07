# Dataset Profile

## 1. Dataset Overview

**Dataset:** Telco Customer Churn

**Problem Type:** Binary Classification

**Domain:** Telecommunications / Customer Retention

**Observations:** 7,043 customers

**Columns:** 21

**Input Features:** 20

**Target Variable:** `Churn`

---

## 2. Business Problem

The objective of this project is to predict whether a telecom customer is likely to churn.

Customer churn occurs when a customer stops using the company's services.

A churn prediction system can help a telecom company identify customers who may leave and allow the business to take proactive retention actions.

---

## 3. Target Variable

The target variable is:

`Churn`

Possible values:

- `Yes` → Customer churned
- `No` → Customer did not churn

For machine learning, this will later be converted into a binary representation:

- `Yes` → `1`
- `No` → `0`

The target transformation will be performed during the preprocessing stage.

---

## 4. Target Distribution

| Churn | Count | Percentage |
|---|---:|---:|
| No | 5,174 | 73.46% |
| Yes | 1,869 | 26.54% |
| **Total** | **7,043** | **100.00%** |

### Observation

The target variable is imbalanced.

Approximately:

- 73.46% of customers did not churn.
- 26.54% of customers churned.

Therefore, accuracy alone will not be sufficient for evaluating the final model.

The project will pay particular attention to:

- Recall
- Precision
- F1-score
- ROC-AUC
- Confusion Matrix

Recall for the churn class is especially important because failing to identify a customer who is likely to churn may result in a missed retention opportunity.

---

## 5. Feature Groups

### 5.1 Customer Demographics

- `gender`
- `SeniorCitizen`
- `Partner`
- `Dependents`

These features describe basic customer demographic and household information.

---

### 5.2 Account Information

- `tenure`
- `Contract`
- `PaperlessBilling`
- `PaymentMethod`

These features describe the customer's relationship and account configuration with the telecom provider.

---

### 5.3 Services

- `PhoneService`
- `MultipleLines`
- `InternetService`
- `OnlineSecurity`
- `OnlineBackup`
- `DeviceProtection`
- `TechSupport`
- `StreamingTV`
- `StreamingMovies`

These features describe the services subscribed to by each customer.

---

### 5.4 Billing

- `MonthlyCharges`
- `TotalCharges`

These features represent the customer's billing information.

---

### 5.5 Customer Identifier

- `customerID`

`customerID` uniquely identifies each customer.

It is an identifier rather than a meaningful predictive feature and will require consideration during the preprocessing/modeling stages.

---

## 6. Observed Data Types

The dataset currently contains:

### Numerical Features

- `SeniorCitizen` → `int64`
- `tenure` → `int64`
- `MonthlyCharges` → `float64`

### String/Categorical Features

Most remaining columns are represented as `str`.

These include:

- `gender`
- `Partner`
- `Dependents`
- `PhoneService`
- `MultipleLines`
- `InternetService`
- `OnlineSecurity`
- `OnlineBackup`
- `DeviceProtection`
- `TechSupport`
- `StreamingTV`
- `StreamingMovies`
- `Contract`
- `PaperlessBilling`
- `PaymentMethod`
- `Churn`
- `customerID`

### Data Type Requiring Investigation

`TotalCharges` is currently loaded as `str`.

Although `TotalCharges` represents a monetary/numerical quantity, its current data type is string.

This will be investigated during the Data Validation stage.

No transformation is performed during the Dataset Understanding stage.

---

## 7. Missing Values

According to the initial `DataFrame.info()` inspection, all 7,043 rows contain non-null values for every column.

However, null values are not the only possible form of missing data.

The Data Validation stage will also investigate:

- Empty strings
- Whitespace values
- Invalid numerical values
- Unexpected categorical values
- Other malformed records

---

## 8. Initial Observations

The initial dataset inspection identified the following:

1. The dataset contains 7,043 customer records.
2. The dataset contains 20 input features and one target variable.
3. The dataset contains both numerical and categorical features.
4. `Churn` is the binary classification target.
5. The target distribution is imbalanced, with 26.54% churned customers.
6. `TotalCharges` is represented as a string even though it represents a numerical quantity.
7. `customerID` is an identifier and should not normally be used as a predictive feature.
8. No null values were reported by the initial `DataFrame.info()` inspection.
9. Further validation is required before preprocessing and model training.

---

## 9. Stage 03 Conclusion

The dataset structure and business meaning have been identified.

At this stage, the raw dataset has **not been modified**.

The next stage will focus on validating whether the dataset is suitable for machine learning.

### Next Stage

**Stage 04 — Data Validation**

Validation will cover:

- Schema validation
- Column validation
- Data type validation
- Missing-value validation
- Empty/whitespace values
- Invalid numerical values
- Categorical value validation
- Duplicate records
- Duplicate customer IDs
- Target integrity
- Data quality summary