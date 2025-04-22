import pandas as pd
import numpy as np

# Load the dataset
cra_df = pd.read_csv('/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis/customer_repayment_data.csv')

# Preview data
print(cra_df.head())
print(cra_df.info())



# Feature Engineering
# Convert dates
cra_df['due_date'] = pd.to_datetime(cra_df['due_date'])
cra_df['paid_date'] = pd.to_datetime(cra_df['paid_date'])

# Calculate delay in days
cra_df['days_late'] = (cra_df['paid_date'] - cra_df['due_date']).dt.days
cra_df['late_payment'] = cra_df['days_late'] > 0

# Calculate repayment success ratio
cra_df['repayment_ratio'] = cra_df['amount_paid'] / cra_df['amount_due']



#KPI Calculations

# Overall Repayment Success Rate
success_rate = (cra_df['amount_paid'].sum() / cra_df['amount_due'].sum()) * 100
print(f"Repayment Success Rate: {success_rate:.2f}%")

# Late Payment Ratio
late_ratio = cra_df['late_payment'].mean() * 100
print(f"Late Payment Ratio: {late_ratio:.2f}%")

# Average Days Late (only where days_late > 0)
avg_days_late = cra_df[cra_df['days_late'] > 0]['days_late'].mean()
print(f"Average Days Late: {avg_days_late:.2f}")

# High Risk Customers
high_risk_count = cra_df[cra_df['risk_score'] > 0.6]['customer_id'].nunique()
print(f"High-Risk Customer Count: {high_risk_count}")



#Monthly Repayment Trends

cra_df['month'] = cra_df['due_date'].dt.to_period('M')
monthly_trend = cra_df.groupby('month')[['amount_due', 'amount_paid']].sum()
monthly_trend['success_rate'] = (monthly_trend['amount_paid'] / monthly_trend['amount_due']) * 100
print(monthly_trend)



# Region-wise and Product-wise Analysis

region_group = cra_df.groupby('region')[['amount_due', 'amount_paid']].sum()
region_group['success_rate'] = (region_group['amount_paid'] / region_group['amount_due']) * 100
print("\nRegion-wise Success Rate:")
print(region_group)

product_group = cra_df.groupby('product_type')[['amount_due', 'amount_paid']].sum()
product_group['success_rate'] = (product_group['amount_paid'] / product_group['amount_due']) * 100
print("\nProduct-wise Success Rate:")
print(product_group)
