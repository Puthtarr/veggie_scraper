import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 🚀 ตั้งค่า Browser (headless)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🌽 ลิงก์สินค้าจากตลาดสี่มุมเมือง
products = {
    "แครอทจีน": "https://www.simummuangmarket.com/product/2678",
    "แครอทไทย": "https://www.simummuangmarket.com/product/2739",
    "ผักกาดขาว(ลุ้ย)": "https://www.simummuangmarket.com/product/79",
    "ผักกาดขาว(ลุ้ย)จีน": "https://www.simummuangmarket.com/product/2680",
    "กรีนโอ๊ค": "https://www.simummuangmarket.com/product/2785",
    "ผักเรดโอ๊ค": "https://www.simummuangmarket.com/product/90",
    "กรีนคอส": "https://www.simummuangmarket.com/product/69",
    "กะหล่ำปลี ม่วง": "https://www.simummuangmarket.com/product/71",
    "ข้าวโพดหวานแกะเม็ด": "https://www.simummuangmarket.com/product/2694"
}

# 📋 รวบรวมผลลัพธ์
results = []

for name, url in products.items():
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 🔍 ดึงราคา
        price_div = soup.find("div", class_="price text-red")
        price = price_div.find("strong").text.strip() if price_div else "ไม่มีข้อมูล"

        results.append(f"{name} : {price} บาท /กก.")

    except Exception as e:
        results.append(f"{name} : ❌ error ({e.__class__.__name__})")

# 🔚 ปิด browser
driver.quit()

# 📧 ส่งอีเมล
gmail_user = "piyaphatputt01@gmail.com"
gmail_pass = "appplxkrntoixxarmazk"
to_email = 'mojikatiya@gmail.com, tanayus.ohm1023@gmail.com, piyaphatputt01@gmail.com'

# 📅 วันที่ปัจจุบัน
report_date = datetime.now().strftime("%d %B %Y")

# 📨 เนื้อหาอีเมล
header = f"""
📆 รายงานวันที่: {report_date}
📊 แหล่งข้อมูล: ตลาดสี่มุมเมือง (www.simummuangmarket.com)

📋 ราคาผักวันนี้
"""

body = header + "\n" + "\n".join(results)
print(results)

msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to_email
msg['Subject'] = "📬 รายงานราคาผักประจำวันที่"
msg.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)
        print("📨 ส่งอีเมลเรียบร้อยแล้ว")
except Exception as e:
    print(f"❌ Error: {e}")
