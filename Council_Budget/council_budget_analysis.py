# Import necessary libraries
import pandas as pd            # For data manipulation and analysis
import matplotlib.pyplot as plt # For creating static, animated, and interactive visualizations
import seaborn as sns           # For making statistical graphics
import numpy as np              # For numerical operations
import warnings                 # To handle warnings

# Suppress specific warnings related to deprecated options in pandas
warnings.filterwarnings("ignore", message=".*use_inf_as_na option is deprecated.*")

# Load the data from a CSV file into a pandas DataFrame
file_path = r'D:\Tech Portfolio\Python Files\council-budget-21-22.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame to understand its structure
print("First few rows of the dataset:")
print(df.head())

# Display basic information about the dataset, such as number of columns, column names, data types, and non-null counts
print("\nDataset Information:")
print(df.info())

# Display summary statistics of the dataset, including count, mean, standard deviation, min, and max values
print("\nSummary Statistics:")
print(df.describe())

# Check for missing values in the dataset
print("\nMissing Values:")
print(df.isnull().sum())

# Data Cleaning

# Fill missing values with 0 (adjust this step as needed based on the actual data)
df = df.fillna(0)

# Ensure 'Amount' column is of numeric type and fill any conversion errors with 0
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

# Remove rows where 'Amount' is negative to ensure only non-negative values are used
df = df[df['Amount'] >= 0]

# Convert any infinite values in the DataFrame to NaN, then fill those NaN values with 0
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# Exploratory Data Analysis (EDA)

# Plotting the distribution of budget amounts using a histogram with a kernel density estimate (KDE)
plt.figure(figsize=(10, 6))
sns.histplot(df['Amount'], bins=30, kde=True)
plt.title('Distribution of Budget Amounts')
plt.xlabel('Budget Amount')
plt.ylabel('Frequency')
plt.show()

# Analyzing the total budget allocation by service
# Grouping the data by 'Service' and summing the 'Amount' for each service
budget_by_service = df.groupby('Service')['Amount'].sum().sort_values(ascending=False)
print("\nBudget by Service:")
print(budget_by_service)

# Visualizing the total budget allocation by service using a bar plot
plt.figure(figsize=(12, 8))
budget_by_service.plot(kind='bar')
plt.title('Total Budget Allocation by Service')
plt.xlabel('Service')
plt.ylabel('Total Budget Allocation')
plt.xticks(rotation=45)
plt.show()

# Additional Analysis

# Calculating the percentage of the total budget for each service
total_budget = df['Amount'].sum()
budget_by_service_percentage = (budget_by_service / total_budget) * 100

# Ensure no negative values in the percentage calculation
budget_by_service_percentage = budget_by_service_percentage[budget_by_service_percentage >= 0]

# Visualizing the percentage of the total budget by service using a pie chart
plt.figure(figsize=(12, 8))
budget_by_service_percentage.plot(kind='pie', autopct='%1.1f%%')
plt.title('Percentage of Total Budget by Service')
plt.ylabel('')
plt.show()

# Conclusion

# Summarize key findings and potential recommendations based on the analysis
print("\nConclusion:")
print("1. The service with the highest budget allocation is {}.".format(budget_by_service.idxmax()))
print("2. The service with the lowest budget allocation is {}.".format(budget_by_service.idxmin()))
print("3. The majority of the budget is allocated to the {} service, accounting for {:.2f}% of the total budget.".format(budget_by_service_percentage.idxmax(), budget_by_service_percentage.max()))
print("Recommendations can be based on these insights, such as suggesting reallocation or further investigation into services with high or low budgets.")

# Save the cleaned data to a new CSV file for future use
cleaned_file_path = r'D:\Tech Portfolio\Python Files\cleaned_council_budget_21_22.csv'
df.to_csv(cleaned_file_path, index=False)
print(f"\nCleaned data saved to {cleaned_file_path}")
