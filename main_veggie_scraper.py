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

        results.append((name, price + " บาท /กก."))

    except Exception as e:
        results.append((name, f"❌ error ({e.__class__.__name__})"))

# 🔚 ปิด browser
driver.quit()

# 📧 ส่งอีเมล
gmail_user = os.getenv("GMAIL_USER")
gmail_pass = os.getenv("GMAIL_PASS")
to_email = 'piyaphatputt01@gmail.com'

# 📅 วันที่ปัจจุบัน
report_date = datetime.now().strftime("%d %B %Y")

# ✨ สร้าง HTML Table สำหรับเนื้อหาอีเมล
table_rows = "".join([f"<tr><td>{name}</td><td>{price}</td></tr>" for name, price in results])

html_body = f"""
<html>
  <body>
    <h2>📆 รายงานราคาผักประจำวันที่: {report_date}</h2>
    <p>📊 แหล่งข้อมูล: <a href="https://www.simummuangmarket.com/">ตลาดสี่มุมเมือง</a></p>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse; font-family: Arial;">
      <thead style="background-color:#f2f2f2;">
        <tr>
          <th>ชื่อผัก</th>
          <th>ราคา</th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>
  </body>
</html>
"""

# 📨 สร้างและส่งอีเมล
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to_email
msg['Subject'] = "📬 รายงานราคาผักประจำวันที่"
msg.attach(MIMEText(html_body, 'html'))

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)
        print("📨 ส่งอีเมลเรียบร้อยแล้ว")
except Exception as e:
    print(f"❌ Error: {e}")
