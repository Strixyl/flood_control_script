import pandas as pd

# load data
df = pd.read_csv('flood_control_dataset.csv')

# track row count
print(f"Total rows: {len(df)}")

# remove commas, convert to float
df['Cost'] = df['Cost'].astype(str).str.replace(',', '')
df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

print(f"The 'Cost' column data type is: {df['Cost'].dtype}")

# handle missing value
nan_costs = df[df['Cost'].isnull()]
if len(nan_costs) > 0:
    print(f"Total rows with null Cost: {len(nan_costs)}")
    df = df.dropna(subset=['Cost'])
else:
    print("All Cost values converted successfully.")

# rows after dropping nulls
print(f"Rows after dropping nulls: {len(df)}")

# handle for dupes
initial_rows = len(df)
duplicates = df[df.duplicated()]

if len(duplicates) > 0:
    print(f"Duplicate rows found: {len(duplicates)}")
else:
    print("No duplicate rows found!")

df = df.drop_duplicates()
removed_duplicates = initial_rows - len(df)

#final rows
print(f"Final total rows: {len(df)}")

#wsave date set
df.to_csv('clean_flood_control_dataset.csv', index=False)
print("Cleaned data saved to 'clean_flood_control_dataset.csv'")
