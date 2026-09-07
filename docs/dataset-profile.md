# Dataset Profile

## Dataset

Telco Customer Churn

## Problem Type

Binary Classification

## Observations

7,043 customers

## Features

20 input features

## Target

`Churn`

- `Yes` → Customer churned
- `No` → Customer did not churn

## Feature Categories

### Customer Demographics

- gender
- SeniorCitizen
- Partner
- Dependents

### Account Information

- tenure
- Contract
- PaperlessBilling
- PaymentMethod

### Services

- PhoneService
- MultipleLines
- InternetService
- OnlineSecurity
- OnlineBackup
- DeviceProtection
- TechSupport
- StreamingTV
- StreamingMovies

### Billing

- MonthlyCharges
- TotalCharges

## Initial Observations

- The dataset contains both numerical and categorical features.
- `TotalCharges` requires further investigation because its data type may not represent its intended numerical meaning.
- `Churn` is the binary target variable.
- The target distribution should be examined carefully because class imbalance can affect model evaluation.