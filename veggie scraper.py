from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# --- Chrome Setup ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# --- Open Browser ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.simummuangmarket.com/product/69")

# --- Click "Past 7 days price" ---
wait = WebDriverWait(driver, 15)
tabs = driver.find_elements(By.CLASS_NAME, "v-tabs__item")
for tab in tabs:
    print("TAB TEXT:", tab.text)
    if "Past 7 days" in tab.text:
        tab.click()
        break

# --- wait div table ---
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-scrollable-table")))

# --- get all HTML ---
html = driver.page_source
driver.quit()

# --- Build soup from HTML ---
soup = BeautifulSoup(html, "html.parser")

# find all div.v-scrollable-table and check for "Date"
sections = soup.find_all("div", class_="v-scrollable-table")
target_table = None

for section in sections:
    table = section.find("table")
    if not table:
        continue
    headers = [th.text.strip() for th in table.find_all("th")]
    headers_lower = [h.lower() for h in headers]
    print("headers check:", headers)

    if any("date" in h for h in headers_lower) or any("วันที่" in h for h in headers_lower):
        target_table = table
        break

# convert to DataFrame and save
if target_table:
    headers = [th.text.strip() for th in target_table.find_all("th")]
    rows = []
    for tr in target_table.find_all("tr"):
        cols = [td.text.strip() for td in tr.find_all("td")]
        if cols:
            while len(cols) < len(headers):
                cols.append("")
            rows.append(cols)

    df = pd.DataFrame(rows, columns=headers)
    print("DataFrame past_7_days_prices:")
    print(df)
    df.to_csv("past_7_days_prices.csv", index=False, encoding="utf-8-sig")
    print("\nSave: past_7_days_prices.csv สำเร็จแล้ว")
else:
    print("Can't Find 'Date'")
