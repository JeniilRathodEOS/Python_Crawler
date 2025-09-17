# Brand Banner Scraper 🖼️

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python-based web scraper that automatically discovers and downloads high-quality brand banner images from official brand websites. Originally developed in Node.js + Puppeteer, now migrated to Python using Playwright for better performance and maintainability.

## 🚀 Features

- **Excel Integration**: Reads brand names from Excel files and outputs results
- **Smart URL Discovery**: Automatically guesses homepage URLs (`.com`, `.it`, etc.)
- **Headless Browser Scraping**: Uses Playwright for JavaScript-rendered content
- **Multi-source Image Extraction**:
  - OpenGraph (`og:image`) tags
  - Twitter Card (`twitter:image`) tags
  - Hero/banner `<img>` elements
  - Large images with proper aspect ratios
- **Image Validation**:
  - Minimum width: 600px (preferred: 720px)
  - Wide aspect ratio filtering
  - File size validation (≥10KB)
  - Format support: JPG, PNG, WEBP
- **Concurrent Processing**: Parallel scraping for improved performance
- **Automatic Organization**: Saves images with clean naming conventions

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/brand-banner-scraper.git
   cd brand-banner-scraper
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## 📖 Usage

### Quick Start

1. **Prepare your input file**: Create or update `italy_brands.xlsx` with brand names in the first column of the first sheet.

   | Merchant_Name |
   |---------------|
   | Gucci         |
   | Prada         |
   | Armani        |
   | Versace       |

2. **Run the scraper**
   ```bash
   python scraper.py
   ```

3. **Check results**:
   - Banner images: `images/` directory
   - Results summary: `brand_banners.xlsx`

### Command Line Options

```bash
python scraper.py --help
```

## ⚙️ Configuration

Modify these constants in `scraper.py` to customize behavior:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `INPUT_EXCEL` | Input Excel file path | `italy_brands.xlsx` |
| `OUTPUT_EXCEL` | Output Excel file path | `brand_banners.xlsx` |
| `IMAGE_DIR` | Image save directory | `images/` |
| `MIN_WIDTH` | Minimum image width (px) | `600` |
| `PREFERRED_WIDTH` | Preferred image width (px) | `720` |
| `CONCURRENCY` | Parallel processing limit | `5` |
| `NAV_TIMEOUT` | Page navigation timeout (ms) | `30000` |

## 📁 Project Structure

```
brand-banner-scraper/
├── scraper.py              # Main scraper script
├── requirements.txt        # Python dependencies
├── italy_brands.xlsx      # Input: brand names
├── brand_banners.xlsx     # Output: scraping results
├── images/                # Output: downloaded banners
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── LICENSE               # MIT License
```

## 🔍 How It Works

1. **Data Loading**: Reads brand names from the first column of `italy_brands.xlsx`
2. **URL Generation**: Generates possible homepage URLs for each brand
3. **Web Scraping**: Uses Playwright to visit websites and extract content
4. **Image Discovery**: Searches for banner images using multiple strategies:
   - Meta tags (OpenGraph, Twitter Cards)
   - Hero section images
   - Large images meeting size criteria
5. **Image Validation**: Filters images by dimensions, aspect ratio, and file size
6. **Download & Save**: Downloads best candidates and saves with clean filenames
7. **Results Export**: Generates summary Excel file with scraping results

## 📊 Output Format

### Images Directory
```
images/
├── gucci_banner.jpg
├── prada_banner.png
├── armani_banner.webp
└── ...
```

### Results Excel (`brand_banners.xlsx`)
| Brand | Status | Image Path | URL | Width | Height |
|-------|--------|------------|-----|-------|--------|
| Gucci | Success | images/gucci_banner.jpg | gucci.com | 1200 | 400 |
| Prada | Success | images/prada_banner.png | prada.com | 1000 | 350 |

## 🔧 Troubleshooting

### Common Issues

**Playwright Timeout Errors**
```bash
# Solution: Increase timeout in scraper.py
NAV_TIMEOUT = 60000  # Increase from 30000 to 60000ms
```

**No Images Found**
- Check if the website uses non-standard image markup
- Verify the brand website is accessible
- Try adjusting image size thresholds

**Excel File Errors**
- Ensure `italy_brands.xlsx` exists in the project root
- Check that brand names are in the first column of the first sheet
- Verify file permissions

**Missing Dependencies**
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
playwright install chromium
```

### Debug Mode

Enable verbose logging by modifying the script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (if available)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

This project uses [Black](https://github.com/psf/black) for code formatting:
```bash
pip install black
black scraper.py
```

## 🛣️ Roadmap

- [ ] **Search Engine Fallback**: Add Google/DuckDuckGo search when homepage isn't found
- [ ] **Structured Logging**: Replace print statements with proper logging
- [ ] **Smart Scoring**: Implement ML-based image quality scoring
- [ ] **Multi-sheet Support**: Process multiple Excel sheets
- [ ] **Proxy Support**: Add proxy rotation for restricted sites
- [ ] **API Integration**: Brand directory API integration
- [ ] **GUI Interface**: Simple desktop interface for non-technical users

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) for reliable web scraping
- [OpenPyXL](https://openpyxl.readthedocs.io/) for Excel file handling
- [Pillow](https://pillow.readthedocs.io/) for image processing

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/brand-banner-scraper/issues) page
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Your environment details (OS, Python version)
   - Relevant log output

---

**Made with ❤️ by [Your Name]**