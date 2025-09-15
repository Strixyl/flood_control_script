import pandas as pd

df = pd.read_csv("cleaned_landslide_data.csv")
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')

# countries with higghest lanslide
print("=== TOP 5 COUNTRIES WITH HIGHEST LANDSLIDE FREQUENCY ===")
top_countries = df['country_name'].value_counts().head(5)
for country, count in top_countries.items():
    print(f"{country}: {count}")

#how mnay landslides in philippines
print(f"\n=== LANDSLIDES IN PHILIPPINES ===")
philippines_landslides = df[df['country_name'] == "Philippines"]
print(f"Total landslides in Philippines: {len(philippines_landslides)}")
print("\nList of landslide events:")
for i, (date, location) in enumerate(zip(philippines_landslides['event_date'], 
                                        philippines_landslides['location_description']), 1):
    print(f"{i}. {date.strftime('%Y-%m-%d')}: {location}")

# how mnay occured before 2007
print(f"\n=== LANDSLIDES BEFORE 2007 ===")
before_2007 = df[df['event_date'] < '2007-01-01']
print(f"Total landslides before 2007: {len(before_2007)}")
print(f"This represents {len(before_2007)/len(df)*100:.1f}% of all recorded landslides")