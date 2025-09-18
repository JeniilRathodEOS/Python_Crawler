# 🖼️ Hero Banner & Logo Scraper

This project extracts **hero banner images** and **logos** from merchant websites.  
It uses **Playwright** (dynamic content), **BeautifulSoup** (static fallback), and DuckDuckGo (final fallback).

---

## 📂 Project Structure
```bash 
TravelMoney/
├── scripts/
│ └── new_condition_css.py # Main script
├── data/
│ └── Book.csv # Input CSV (merchant_name, merchant_website)
├── output/
│ └── banners_res_4/ # Output images + results.csv
├── requirements.txt # Dependencies
└── README.md

```
---

## ⚙️ Installation
```bash
1. Clone the repo:

   git clone https://github.com/JeniilRathodEOS/Python_Crawler.git
   cd Python_Crawler
   git checkout image-scraper-feature

2. Create virtual environment:
    python -m venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows

3.Install Dependencies:
    pip insstall -r requirements.txt

4. Install Playwright browsers:
    playwright install

```

▶️ Usage

Run the script with:
python scripts/new_condition_css.py --csv data/Book.csv --output output/banners_res_4

📝 Output

All accepted banner images → stored in output/banners_res_4/
Rejected images → output/banners_res_4/rejected/
A results CSV → output/banners_res_4/results.csv

results.csv format:
merchant_name	merchant_website	banner_image	source


🚀 Features
    ✅ Extracts <img src> and CSS background-image
    ✅ Handles lazy-loaded images
    ✅ Validates image size, entropy, and text density
    ✅ Falls back to BeautifulSoup → DuckDuckGo if Playwright fails
    ✅ Saves rejected images for review


---

## 5. Add, Commit & Push
```bash
git add scripts/new_condition_css.py data/Book.csv output/banners_res_4/ requirements.txt README.md
git commit -m "Add hero banner scraper script with input/output and docs"
git push origin image-scraper-feature

```
