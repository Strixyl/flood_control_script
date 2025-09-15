import pandas as pd

# Load the dataset
df = pd.read_csv("flood_control_complete_9k_dataset.csv", encoding="utf-8")

print("Initial Shape:", df.shape)

# 1. Handling Missing Values
# ---------------------------------
# Drop columns that are completely empty
df = df.dropna(axis=1, how='all')

# Drop rows that are completely empty
df = df.dropna(axis=0, how='all')

# For partially missing values:
# Option A: Fill with placeholder 'N/A'
df = df.fillna("N/A")

# Option B: For numeric columns, fill with 0 (comment out if not needed)
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col] = df[col].fillna(0)

print("After handling missing values:", df.shape)

# 2. Removing Duplicates
# ---------------------------------
# Remove exact duplicate rows
df = df.drop_duplicates()

# If you want to remove duplicates based on a specific column like "Project Description":
if "Project Description" in df.columns:
    df = df.drop_duplicates(subset=["Project Description"])

print("After removing duplicates:", df.shape)

# 3. Standardizing Data Formats
# ---------------------------------
# Clean column names (remove spaces, unify format)
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# Example: Convert date columns to consistent YYYY-MM-DD format
for col in df.columns:
    if "date" in col.lower():
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")
        except:
            pass

# Example: Standardize text columns (remove extra spaces, make lowercase)
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip().str.lower()

print("After standardizing formats:", df.shape)

# Save cleaned dataset
df.to_csv("flood_control_cleaned.csv", index=False, encoding="utf-8")
df.to_excel("flood_control_cleaned.xlsx", index=False)

print("Cleaning complete!")
print("Final Shape:", df.shape)
