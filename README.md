# Landslide Data Cleaning - README

## Overview
This project focuses on cleaning and improving the **Global Landslide Catalog** dataset. The dataset originally contained inconsistent date formats, duplicate entries, and multiple versions of country names. Through data cleaning, the dataset was transformed into a more reliable foundation for analysis.  

## Why This Cleaning Was Needed
The raw dataset had several challenges:  
- **Inconsistent date formats** (strings, invalid entries, mixed formats).  
- **Multiple country name variations** (e.g., "United States", "United States of America", "USA").  
- **Duplicate event entries** that inflated landslide counts.  
- **Missing critical information** (such as empty country or invalid dates).  

Without cleaning, these issues would lead to misleading analysis results, such as fragmented country rankings or unreliable time-based trends.  

## How It Works
### Data Cleaning Process
1. **Handling Missing Values**  
   - Removed records with missing country names or invalid dates to ensure data completeness.  

2. **Duplicate Removal**  
   - Eliminated duplicate entries based on unique event IDs so each event is only counted once.  

3. **Standardization of Country Names**  
   - Unified different versions of country names (e.g., "Russian Federation" → "Russia").  
   - Ensured consistency for accurate geographic aggregation.  

4. **Date Format Standardization**  
   - Converted all event dates into proper datetime objects.  
   - Invalid dates were dropped.  
   - Created two new variables: **Event Time** and **Cleaned Event Date**.  

## Data Quality Improvements
- **Size Reduction** – Focused dataset with only reliable entries.  
- **Geographic Standardization** – Country names consolidated, preventing split counts.  
- **Temporal Consistency** – Dates standardized, allowing accurate time-based analysis.  
- **Duplicate Elimination** – No more inflated landslide frequencies.  

## Impact on Analysis
- **Accurate Country Rankings** – Standardization prevented fragmented counts (e.g., USA grouped correctly).  
- **Reliable Temporal Trends** – Pre-2007 and other date-based analyses are now trustworthy.  
- **Improved Philippines Analysis** – All entries consolidated under a single name for accurate regional counts.  

## Future Enhancements
- Add geographic coordinates for mapping and spatial analysis.  
- Integrate rainfall and climate data for trigger analysis.  
- Build interactive dashboards (maps, time series, heatmaps).  
- Develop predictive models to identify high-risk zones.  

