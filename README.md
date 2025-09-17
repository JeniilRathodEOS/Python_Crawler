# 🖼️ Brand Banner Scraper (Python)

This project is a **Python-based web scraper** that automatically finds and downloads **brand banner images** from their official websites.  
It was originally written in **Node.js + Puppeteer**, but has been converted to **Python** using **Playwright**, **aiohttp**, and **openpyxl**.

---

## ✨ Features

- 📖 Reads **brand names** from an Excel file (`italy_brands.xlsx`)
- 🌍 Guesses likely **homepage URLs** (`brand.com`, `brand.it`, etc.)
- 🕵️ Uses **Playwright** (headless Chromium) to visit websites
- 🔎 Extracts **candidate banner images**:
  - OpenGraph (`og:image`)
  - Twitter (`twitter:image`)
  - Hero/Banner/Main `<img>` tags
  - Other large images (scored by size/aspect ratio)
- ✅ **Validates images**:
  - Minimum width: `600px`
  - Aspect ratio must be wide (not square/tall)
  - Minimum size: `10KB`
  - Allowed formats: JPG, PNG, WEBP
- 💾 Saves banners to `images/` folder
- 📊 Outputs results into `brand_banners.xlsx`
- ⚡ Supports **concurrency** (process multiple brands at once)

---

## 📂 Project Structure

├── italy_brands.xlsx       # Input Excel file (list of brand names in first column)
├── brand_banners.xlsx      # Output Excel file (results)
├── images/                 # Folder where images are saved
├── scraper.py              # Main Python script
└── README.md               # Documentation


---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/brand-banner-scraper.git
   cd brand-banner-scraper


Install dependencies

pip install -r requirements.txt


