import pandas as pd

# Load data
df = pd.read_csv("Global_Landslide_Catalog_Export_rows.csv")
print(f"Original: {len(df)} rows")

# remove row without names
df = df.dropna(subset=['country_name'])
print(f"After removing null countries: {len(df)} rows")

# fi date
df['event_date'] = pd.to_datetime(df['event_date'], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
df = df.dropna(subset=['event_date'])
df['event_time'] = df['event_date'].dt.time
df['event_date'] = df['event_date'].dt.date

# clean country names
df['country_name'] = df['country_name'].str.strip().str.title()
replacements = {
    "United States": "USA",
    "United States Of America": "USA", 
    "Philippines, The": "Philippines",
    "Russian Federation": "Russia",
    "Democratic Republic Of The Congo": "DR Congo",
    "Czechia": "Czech Republic"
}
df['country_name'] = df['country_name'].replace(replacements)

# remvoe dupes
df = df.drop_duplicates(subset=['event_id'])
print(f"Final: {len(df)} rows")

# save csv
df.to_csv("cleaned_landslide_data.csv", index=False)
print("Saved to cleaned_landslide_data.csv")