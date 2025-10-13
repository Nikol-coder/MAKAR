from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import logging
import os
import json

# Configure logging level
logging.getLogger('selenium').setLevel(logging.WARNING)

# Create the main output folder for HTML files
output_folder = "HTML-3-Text"
os.makedirs(output_folder, exist_ok=True)

# Configure Edge browser options
edge_options = Options()
edge_options.add_argument('--disable-blink-features=AutomationControlled')
edge_options.add_argument('--ignore-certificate-errors')
edge_options.add_argument('--disable-extensions')
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option("useAutomationExtension", False)

# Initialize the WebDriver
driver = webdriver.Edge(options=edge_options)

def sanitize_filename(name):
    """Remove or replace illegal filename characters."""
    return "".join(c if c.isalnum() or c in (" ", ".", "_") else "_" for c in name.strip())

# Load the JSON Lines file
json_file_path = "your test.json"
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        # Read line by line in JSON Lines format
        json_data = [json.loads(line) for line in f if line.strip()]
except Exception as e:
    print(f"Failed to load JSON file: {e}")
    exit(1)

# Iterate over the JSON entries
for idx, entry in enumerate(json_data):
    img_id = entry.get('img_id', f"unknown_{idx}")
    base_name = sanitize_filename(os.path.splitext(img_id)[0])
    
    # Use the 'text' field directly as the search query
    search_query = entry.get('text', '').strip()
    if not search_query:
        print(f"Skipping {img_id}: Empty text field")
        continue

    # Create a folder named after img_id
    folder_path = os.path.join(output_folder, base_name)
    os.makedirs(folder_path, exist_ok=True)

    print(f"\nProcessing [{img_id}] Search Query: '{search_query}'")

    try:
        # Open Bing homepage
        driver.get("https://www.bing.com/?cc=us")

        # Wait for the search box to load
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Enter the search query
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.b_algo"))
        )

        # Extract the top 5 result links
        results = driver.find_elements(By.CSS_SELECTOR, "li.b_algo")[:5]
        top_links = []
        for result in results:
            try:
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link.startswith(("http://", "https://")):
                    top_links.append(link)
            except Exception as e:
                print(f"Error extracting link: {e}")

        print(f"[{img_id}] Top 5 links:", top_links)

        # Save the HTML of each linked page
        for i, url in enumerate(top_links):
            try:
                driver.get(url)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                filename = os.path.join(folder_path, f"top_{i+1}.html")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Failed to process {url}: {e}")

    except Exception as e:
        print(f"Search failed for '{search_query}': {e}")
        continue

# Close the browser
driver.quit()