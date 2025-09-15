import pandas as pd
#load dataset
df = pd.read_csv("clean_flood_control_dataset.csv")

highest_cost = df.loc[df['Cost'].idxmax()]
lowest_cost = df.loc[df['Cost'].idxmin()]

print("Project with the highest cost:")
print(highest_cost)

print("\nProject with the lowest cost:")
print(lowest_cost)

# proejct neatr  me (iloilo)
iloilo_projects = df[df['Location'].str.contains("Iloilo", case=False, na=False)]

print(f"\nTotal projects in Iloilo: {len(iloilo_projects)}")
print("\nList of projects in Iloilo:")
print(iloilo_projects)
