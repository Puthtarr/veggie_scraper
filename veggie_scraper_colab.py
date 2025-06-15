import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ตั้งค่า Chrome สำหรับ Colab
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

from selenium.webdriver.chrome.service import Service
driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

# เปิดเว็บ
driver.get("https://www.simummuangmarket.com/product/69")

# คลิกแท็บ Past 7 Days Price
wait = WebDriverWait(driver, 10)
tabs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "v-tabs__item")))
for tab in tabs:
    print("TAB TEXT:", tab.text.strip())
    if "PAST 7 DAYS" in tab.text.upper():
        tab.click()
        break

# รอให้ตารางแสดง
time.sleep(2)
soup = BeautifulSoup(driver.page_source, "html.parser")
tables = soup.find_all("table", class_="search-result-table w-100")

target_table = None
for table in tables:
    headers = [th.text.strip().lower() for th in table.find_all("th")]
    print("📌 ตรวจสอบ headers:", headers)
    if any("date" in h or "วันที่" in h for h in headers):
        target_table = table
        break

driver.quit()

# แปลงเป็น DataFrame
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
    print(df)
else:
    print("❌ ไม่เจอตารางราคาย้อนหลัง")
