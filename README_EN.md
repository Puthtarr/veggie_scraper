# 🥦 veggie_scraper

**Automated daily vegetable price tracker**  
This project uses Python and GitHub Actions to scrape vegetable prices from the "Si Mum Mueang Market" website and send a daily report via email.  
Future support includes LINE Notify or LINE Bot integration.

---

## 📌 Features

- ✅ Web scraping vegetable prices from [www.simummuangmarket.com](https://www.simummuangmarket.com)
- ✅ Sends daily email reports in HTML table format
- ✅ Automatically runs every day at 10:00 AM (Thailand time) using GitHub Actions
- 🧱 Written in Python using BeautifulSoup and Selenium (Headless Chrome)
- ☁️ No local machine required — runs free on GitHub Actions

---

## 🛠️ Tech Stack

| Tool             | Usage                            |
|------------------|----------------------------------|
| Python 3.10       | Main scripting language          |
| Selenium          | Headless browser automation      |
| BeautifulSoup4    | HTML parsing and data extraction |
| GitHub Actions    | Automation and scheduling        |
| Gmail (SMTP)      | Sending email reports            |
| Webdriver Manager | Automatic ChromeDriver setup     |

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Puthtarr/veggie_scraper.git
cd veggie_scraper
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables (for local use)
Create a `.env` file with the following:

```
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password
```

> 🔐 Requires Gmail with 2FA enabled and an App Password

### 4. Run the Script
```bash
python main_veggie_scraper.py
```

---

## 🚀 Automated GitHub Actions

### 🔐 Set up GitHub Secrets

Go to `Settings > Secrets and variables > Actions` and add:

| Secret Name   | Example                   |
|---------------|---------------------------|
| `GMAIL_USER`  | `your_email@gmail.com`    |
| `GMAIL_PASS`  | `appplxkrntoixxarmazk`    |

### 📅 Scheduled Execution (cron)

In `.github/workflows/python-script.yml`:

```yaml
schedule:
  - cron: "0 3 * * *"  # 10:00 AM Thailand Time (03:00 UTC)
```

---

## 📬 Sample Email Output

| Vegetable Name     | Price          |
|--------------------|----------------|
| Carrot (China)     | 25 THB/kg      |
| Red Oak Lettuce    | 100 THB/kg     |
| ...                | ...            |

---

## 💡 Potential Extensions

- LINE Bot or LINE Notify integration
- Attach CSV or Google Sheets
- View historical data with Superset or Looker Studio

---

## 🙌 Developer

Piyaphat Putthasangwan  
GitHub: [@Puthtarr](https://github.com/Puthtarr)
