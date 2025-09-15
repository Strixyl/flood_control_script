from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def load_all_9k_data():
    options = Options()
    # options.add_argument('--headless')  # Keep visible to monitor progress
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://sumbongsapangulo.ph")
        time.sleep(10)
        
        all_data = []
        
        # Method 1: Aggressive pagination and infinite scroll
        print("Loading ALL data - this may take several minutes...")
        
        previous_count = 0
        consecutive_no_change = 0
        max_attempts = 500  # Increased for 9K+ records
        
        for attempt in range(max_attempts):
            # Scroll to bottom multiple times
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # Try clicking ALL possible load/pagination buttons
            load_button_selectors = [
                "//button[contains(text(), 'Load')]",
                "//button[contains(text(), 'More')]", 
                "//button[contains(text(), 'Next')]",
                "//a[contains(text(), 'Load')]",
                "//a[contains(text(), 'More')]",
                "//a[contains(text(), 'Next')]",
                "//span[contains(text(), 'Load')]",
                "//div[contains(text(), 'Load')]",
                ".pagination a", ".pagination button",
                ".load-more", ".btn-load", ".show-more",
                "[data-load]", "[data-more]", "[onclick*='load']"
            ]
            
            buttons_clicked = 0
            for selector in load_button_selectors:
                try:
                    if selector.startswith("//"):
                        buttons = driver.find_elements(By.XPATH, selector)
                    else:
                        buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for button in buttons:
                        if button.is_displayed() and button.is_enabled():
                            try:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                                time.sleep(0.5)
                                driver.execute_script("arguments[0].click();", button)
                                time.sleep(2)
                                buttons_clicked += 1
                            except:
                                continue
                except:
                    continue
            
            # Try numeric pagination (page 1, 2, 3, etc.)
            for page_num in range(2, 101):  # Try pages 2-100
                page_buttons = driver.find_elements(By.XPATH, f"//a[text()='{page_num}'] | //button[text()='{page_num}']")
                for page_btn in page_buttons:
                    try:
                        if page_btn.is_displayed():
                            driver.execute_script("arguments[0].click();", page_btn)
                            time.sleep(3)
                            buttons_clicked += 1
                            break
                    except:
                        continue
            
            # Check current data count
            current_rows = driver.find_elements(By.TAG_NAME, "tr")
            current_count = len(current_rows)
            
            if current_count > previous_count:
                print(f"Progress: {current_count} rows loaded (attempt {attempt + 1})")
                previous_count = current_count
                consecutive_no_change = 0
            else:
                consecutive_no_change += 1
            
            # Stop if no new data for multiple attempts
            if consecutive_no_change >= 10 and current_count > 100:
                print(f"No new data for {consecutive_no_change} attempts. Stopping at {current_count} rows.")
                break
            
            if buttons_clicked == 0 and consecutive_no_change >= 5:
                break
        
        # Method 2: Extract ALL loaded data
        print("Extracting all loaded data...")
        
        # Get all tables
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"Found {len(tables)} tables")
        
        for table_idx, table in enumerate(tables):
            try:
                rows = table.find_elements(By.TAG_NAME, "tr")
                print(f"Table {table_idx + 1}: Processing {len(rows)} rows...")
                
                if len(rows) > 1:
                    # Get headers from first row
                    header_cells = rows[0].find_elements(By.XPATH, ".//th | .//td")
                    headers = []
                    for i, cell in enumerate(header_cells):
                        text = cell.text.strip()
                        if text:
                            headers.append(text)
                        else:
                            headers.append(f"Column_{i}")
                    
                    # Process all data rows
                    for row in rows[1:]:
                        cells = row.find_elements(By.XPATH, ".//td | .//th")
                        data = [cell.text.strip() for cell in cells]
                        
                        if data and any(d.strip() for d in data if d):
                            row_dict = {}
                            for i, value in enumerate(data):
                                if i < len(headers):
                                    row_dict[headers[i]] = value
                                else:
                                    row_dict[f"Extra_Col_{i}"] = value
                            all_data.append(row_dict)
                            
            except Exception as e:
                print(f"Error processing table {table_idx}: {e}")
                continue
        
        print(f"Raw data collected: {len(all_data)} records")
        
        # Method 3: Remove duplicates
        seen = set()
        unique_data = []
        
        for item in all_data:
            if isinstance(item, dict):
                # Create unique key based on project description
                key = item.get('Project Description', '') or item.get('content', '') or str(sorted(item.items()))
                if key and key not in seen:
                    seen.add(key)
                    unique_data.append(item)
        
        print(f"Unique records: {len(unique_data)}")
        
        if unique_data:
            # Create DataFrame
            df = pd.DataFrame(unique_data)
            
            # Remove completely empty columns
            df = df.dropna(axis=1, how='all')  # Drop columns that are all NaN
            df = df.loc[:, (df != '').any(axis=0)]  # Drop columns that are all empty strings
            
            # Remove columns that are mostly empty (less than 5% data)
            threshold = len(df) * 0.05
            df = df.dropna(axis=1, thresh=threshold)
            
            # Clean column names
            df.columns = [col.strip() if col and col.strip() else f'Column_{i}' 
                         for i, col in enumerate(df.columns)]
            
            # Remove the empty column you mentioned (likely just '')
            if '' in df.columns:
                df = df.drop('', axis=1)
            
            # Save complete dataset
            df.to_csv("flood_control_complete_9k_dataset.csv", index=False, encoding='utf-8')
            df.to_excel("flood_control_complete_9k_dataset.xlsx", index=False)
            
            print(f"\n✅ SUCCESS! Saved {len(unique_data)} records")
            print(f"📊 Columns: {list(df.columns)}")
            print(f"📁 Files: flood_control_complete_9k_dataset.csv/.xlsx")
            print(f"🎯 Dataset shape: {df.shape}")
            
            return df
        else:
            print("No available data, no data extracted")
            return None
            
    except Exception as e:
        print(f" Error: {e}")
        return None
    
    finally:
        driver.quit()

# Execute the complete data loader
print(" Gathering Data.")
dataset = load_all_9k_data()