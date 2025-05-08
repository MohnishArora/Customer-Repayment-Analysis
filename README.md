# 💡 Customer Repayment Analysis – EDA & Feature Engineering

This project is aimed at understanding customer repayment behavior using Python for data analysis and feature engineering. The goal is to extract meaningful patterns and prepare the data for dashboard visualization and business insights.

---

## 📁 Project Structure

```
📂 Customer_Retention_Analysis/
│
├── Data.py                                       # Python script for EDA
├── customer_repayment_data.csv                   # Original raw dataset
├── customer_repayment_data_updated.csv           # Data with new features
├── Reworked_Customer_Repayment_Analysis.xlsx     # Combined Excel output with all sheets
├── README.md                                     # This file
```

---

## 🧪 Environment & Tools

- **Editor:** VS Code
- **Language:** Python
- **Libraries Used:** `pandas`, `numpy`
- **Data Source:** Simulated repayment data with 50,000 rows

---

## 🔍 Step-by-Step EDA in Python

Below are the 6 steps I followed to clean, transform, and analyze the dataset before building a BI dashboard.

---

### ✅ **Step 1: Load the Data**

Used Pandas to load the dataset and get a first look at its structure.

```python
import pandas as pd

df = pd.read_csv("customer_repayment_data.csv")

print(df.head())            # See first 5 rows
print(df.info())            # Column types and nulls
print(df.describe())        # Summary statistics
print(df.isnull().sum())    # Check for missing values
```

**Goal:** Understand column types, spot any missing values, and inspect the data format.

---

### ✅ **Step 2: Convert Date Columns**

Converted the `due_date` and `paid_date` from text (object) format into proper date format using `pd.to_datetime()`.

```python
df['due_date'] = pd.to_datetime(df['due_date'])
df['paid_date'] = pd.to_datetime(df['paid_date'])
```

**Why?** This allows us to calculate delays and group data by month, year, etc.

---

### ✅ **Step 3: Feature Engineering**

Created new columns to uncover payment behavior.

```python
df['days_late'] = (df['paid_date'] - df['due_date']).dt.days
df['late_payment'] = df['days_late'] > 0
df['repayment_ratio'] = df['amount_paid'] / df['amount_due']
df['month'] = df['due_date'].dt.to_period('M')
```

**Why?**

- `days_late`: How many days a payment was delayed
- `late_payment`: Boolean (True/False) if payment was late
- `repayment_ratio`: Percentage of (amount paid vs due)
- `month`: Extracted for monthly analysis

---

### ✅ **Step 4: Key Performance Indicators (KPIs)**

Calculated high-level metrics using the engineered features.

```python
success_rate = (df['amount_paid'].sum() / df['amount_due'].sum()) * 100
late_ratio = df['late_payment'].mean() * 100
avg_days_late = df[df['days_late'] > 0]['days_late'].mean()
high_risk_customers = df[df['risk_score'] > 0.6]['customer_id'].nunique()
```

**Why?** These KPIs help measure repayment performance across the entire customer base.

---

### ✅ **Step 5: Monthly Repayment Trends**

Grouped repayment data by month to track performance over time.

```python
monthly = df.groupby('month')[['amount_due', 'amount_paid']].sum()
monthly['repayment_success'] = (monthly['amount_paid'] / monthly['amount_due']) * 100
monthly.to_csv("monthly_trends.csv")
```

**Why?** Understand how repayment patterns change over time. Helps in identifying seasonality or behavioral shifts.

---

### ✅ **Step 6: Region-wise & Product-wise Analysis**

Grouped data to compare repayment success by region and product type.

```python
region = df.groupby('region')[['amount_due', 'amount_paid']].sum()
region['repayment_success'] = (region['amount_paid'] / region['amount_due']) * 100
region.to_csv("region_trends.csv")

product = df.groupby('product_type')[['amount_due', 'amount_paid']].sum()
product['repayment_success'] = (product['amount_paid'] / product['amount_due']) * 100
product.to_csv("product_trends.csv")
```

**Why?** Useful for targeting interventions or campaigns by region or product.

---

## 📆 Final Output

✅ **customer\_repayment\_data\_updated.csv**

> Contains all the new features created during EDA

✅ **customer\_repayment\_analysis.xlsx**

> One Excel file with separate sheets for:

- Full dataset
- Monthly trends
- Region-level and product-level repayment analysis

---

## 🚀 What's Next

This cleaned and enriched dataset will be used to build an **interactive Power BI dashboard** showcasing KPIs and trends for business stakeholders.

---

## Author

**Mohnish Arora**\
MSMIS | Data Engineering & Business Intelligence\
[LinkedIn](#) | [GitHub](#)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

