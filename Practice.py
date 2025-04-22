import pandas as pd
import numpy as np


# 1. Load dataset
df = pd.read_csv('/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis/customer_repayment_data.csv')



# 2. Basic commands to check loaded data 

print(df.head())        # Preview of the data (Preview or Head funtion)
print(df.info())        # Data Types + non-null counts (Info Summary function)
#print(df.describe())    # Stats summary of number data type fields (Descriptive Statistics Summary)
#print(df.isnull().sum()) # Missing values check (Missing Value Count)

# We have performed Data summary and Inspection functions above. 
# These are the 1st steps in any analysis pipeline.
# They are commonly used Exploratory Data Analysis (EDA) functions in Pandas



# 3. Changing data types
# After performing basic EDA, we found incorrect data type used for date columns.
# To correct this we use Python in-built module of datetime to change data type to date

# Convert to datetime
df['due_date'] = pd.to_datetime(df['due_date'])
df['paid_date'] = pd.to_datetime(df['paid_date'])

print(df.info()) # Shows the data type of Dates changed to date format from objects



# 4. Feature Engineering
# Once we have all the data in correct format we are set to move ahead with next step.
# Next Step: Feature Engineering — a fundamental concept in both data analysis and machine learning.
# A process of creating new meaningful columns (features) from existing data to help with analysis, modeling, or visualization.

df['days_late'] = (df['paid_date'] - df['due_date']).dt.days
# New numeric feature to quantify how late a payment is. 
# Helps in calculating average delay, analyzing repayment behavior, etc.

df['late_payment'] = df['days_late'] > 0
#New boolean feature (True/False) indicating whether the payment was late. 
# Useful for computing late payment ratio.

df['repayment_ratio'] = df['amount_paid'] / df['amount_due']
# New ratio feature showing how much of the due amount was actually paid. 
# Great for assessing repayment behavior per customer or region.
print(df.info())

# This completes the feature engineering part where we have used raw data to create features 
# useful for analysing data. Next step is creating KPIs using this features.



# 5. KPIs - Key Performance Indicators

# A. Repayment Success Rate
success_rate = (df['amount_paid'].sum() / df['amount_due'].sum()) * 100
# What it shows: The overall percentage of money repaid out of the total due.
# Why it's useful: It tells you how effectively customers are paying back their dues.

print(f"Repayment Success Rate: {success_rate:.2f}%")

# B. Late Payment Ratio
late_ratio = df['late_payment'].mean() * 100
#What it shows: The percentage of payments made after the due date.
# Why it's useful: Helps assess the punctuality of customer repayments and potential credit risk.

print(f"Late Payment Ratio: {late_ratio:.2f}%")

# C. Average Days Late
avg_days_late = df[df['days_late'] > 0]['days_late'].mean()
# What it shows: How many days, on average, customers pay late. 
# Why it's useful: It quantifies how late late payers really are — useful for planning interventions or reminders.

print(f"Average Days Late: {avg_days_late:.2f} days")

# D. High-Risk Customer Count
high_risk_count = df[df['risk_score'] > 0.6]['customer_id'].nunique()
# What it shows: The number of unique customers with a risk score above 0.6.
# Why it's useful: Helps segment at-risk customers and plan strategies to improve their repayment behavior.

print(f"High-Risk Customers: {high_risk_count}")




# 6. Repayment Trends

# Monthly
df['month'] = df['due_date'].dt.to_period('M')
monthly = df.groupby('month')[['amount_due', 'amount_paid']].sum()
monthly['repayment_success'] = (monthly['amount_paid'] / monthly['amount_due']) * 100
print(monthly.head())

# Region
region = df.groupby('region')[['amount_due', 'amount_paid']].sum()
region['repayment_success'] = (region['amount_paid'] / region['amount_due']) * 100
print(region)

# Product Type
product = df.groupby('product_type')[['amount_due', 'amount_paid']].sum()
product['repayment_success'] = (product['amount_paid'] / product['amount_due']) * 100
print(product)



# 7. Exporting the updated data
# Once we have completed the EDA & Feature Engg and created new DataFrames like monthly, 
# region, and product, we can export each to CSV easily using pandas.

df.to_csv("/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis/customer_repayment_data_updated.csv", index=False)


#monthly.to_csv("/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis/monthly.csv", index=True)
#region.to_csv("/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis", index=True)
#product.to_csv("/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis", index=True)


# To export updated data into 1 single workbook
output_path = "/Users/mohnisharora/Documents/github_repos/Customer_Retention_Analysis/Reworked_Customer_Repayment_Analysis.xlsx"

# Write all dataframes into separate sheets
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Full_Data', index=False)
    monthly.to_excel(writer, sheet_name='Monthly_Trend', index=True)
    region.to_excel(writer, sheet_name='Region_Analysis', index=True)
    product.to_excel(writer, sheet_name='Product_Analysis', index=True)

print("All sheets written to Excel successfully!")
