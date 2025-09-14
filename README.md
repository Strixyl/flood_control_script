Flood Control Data Scraper - README
Overview
This script automatically extracts all 9,000+ flood control project records from the Philippine government website sumbongsapangulo.ph and saves them to CSV and Excel files.
Why This Script is Needed
Unlike datasets available on Kaggle or other platforms, this government website doesn't provide a direct download option. The data is displayed in tables with pagination and "Load More" functionality, making manual extraction impractical for 9,000+ records.
How It Works
1. Auto-Loading Data
# Scrolls to bottom to trigger lazy loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Automatically clicks "Load More" buttons
buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Load')]")
for button in buttons:
    driver.execute_script("arguments[0].click();", button)


What this does: Simulates human behavior of scrolling down and clicking "Load More" buttons to load all data pages.
2. Auto-Pagination
# Clicks through page numbers (1, 2, 3, etc.)
for page_num in range(2, 101):
    page_buttons = driver.find_elements(By.XPATH, f"//a[text()='{page_num}']")
    driver.execute_script("arguments[0].click();", page_btn)What this does: Automatically clicks through numbered page links to access all data pages.

3. Data Extraction
# Finds all tables on the page
tables = driver.find_elements(By.TAG_NAME, "table")

# Extracts headers and data from each table
headers = [cell.text.strip() for cell in header_cells]
data = [cell.text.strip() for cell in data_cells]
row_dict = dict(zip(headers, data))  # Combines headers with dataWhat this does: Reads HTML table structure and converts it to structured data (dictionaries).

4. Data Cleaning & Export
# Removes duplicate records
if key not in seen:
    unique_data.append(item)

# Creates DataFrame and removes empty columns
df = pd.DataFrame(unique_data)
df = df.dropna(axis=1, how='all')  # Remove empty columns




# Saves to files
df.to_csv("flood_control_dataset.csv", index=False)
df.to_excel("flood_control_dataset.xlsx", index=False)

What this does: Cleans the data and exports it to both CSV and Excel formats.
Key Code Explanations
XPath vs CSS Selectors
# XPath - searches by text content
"//button[contains(text(), 'Load')]"  # Finds buttons containing "Load"


# CSS Selector - searches by attributes/classes  
".load-more"  # Finds elements with class "load-more"
Element Interaction# Scroll element into view first
driver.execute_script("arguments[0].scrollIntoView();", button)


# Use JavaScript click (more reliable than .click())
driver.execute_script("arguments[0].click();", button)
Progress Monitoring
current_count = len(driver.find_elements(By.TAG_NAME, "tr"))
if current_count > previous_count:
    print(f"Progress: {current_count} rows loaded")


What this does: Counts table rows to track loading progress and know when to stop.
Installation & Usage
Prerequisites
pip install selenium pandas openpy
Run the Script
python flood_control_scraper.py
Output Files
flood_control_complete_9k_dataset.csv - For analysis tools
flood_control_complete_9k_dataset.xlsx - For Excel/spreadsheet applications
Expected Results
Total Records: 9,000+ flood control projects
Columns: Project Description, Location, Contractor, Cost, Completion Date, etc.
Time: 5-15 minutes depending on internet speed
Troubleshooting
Chrome DevTools messages: Normal browser startup messages - ignore them
"No data found": Website may have changed structure or requires different interaction
Slow performance: Large dataset loading - be patient, script shows progress updates



