import argparse
import asyncio
import csv
import os
import re
import aiohttp
import pytesseract
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from skimage.measure import shannon_entropy
from playwright.async_api import async_playwright

# ------------- CONFIG -------------
MIN_WIDTH = 720
MIN_HEIGHT = 720
MAX_TEXT_RATIO = 0.02
MAX_CONCURRENT = 5
# ----------------------------------

async def fetch(session, url):
    try:
        async with session.get(url, timeout=15) as resp:
            if resp.status == 200:
                return await resp.read()
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
    return None


def evaluate_image(img):
    """Compute metrics: size, entropy, OCR text ratio."""
    w, h = img.size
    if w == 0 or h == 0:
        return None
    arr = np.array(img.convert("RGB"))
    entropy = shannon_entropy(arr)
    try:
        text = pytesseract.image_to_string(img.convert("RGB"))
    except Exception:
        text = ""
    text_ratio = len(text.strip()) / (w * h)
    return {"width": w, "height": h, "entropy": entropy,
            "text_ratio": text_ratio, "area": w * h}


def is_valid_banner(metrics):
    return (
        metrics["width"] >= MIN_WIDTH and
        metrics["height"] >= MIN_HEIGHT and
        metrics["text_ratio"] <= MAX_TEXT_RATIO
    )


async def download_and_check(url, session, output_dir, merchant):
    """Download image, evaluate it, save to accepted or rejected folder."""
    if any(url.lower().endswith(ext) for ext in [".svg", ".ico", ".gif"]):
        return None

    content = await fetch(session, url)
    if not content:
        return None

    try:
        img = Image.open(BytesIO(content))
        metrics = evaluate_image(img)

        fname = f"{merchant}_{os.path.basename(url).split('?')[0]}"
        safe_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', fname)

        if metrics and is_valid_banner(metrics):
            # ✅ Save accepted
            path = os.path.join(output_dir, safe_name)
            img.convert("RGB").save(path, "JPEG")
            return path
        else:
            # ❌ Save rejected
            rejected_dir = os.path.join(output_dir, "rejected")
            os.makedirs(rejected_dir, exist_ok=True)
            rejected_path = os.path.join(rejected_dir, f"rejected_{safe_name}")
            img.convert("RGB").save(rejected_path, "JPEG")
            return None

    except Exception as e:
        print(f"⚠️ Failed to download/evaluate {url}: {e}")
    return None


async def scrape_site_images(playwright, url):
    """Scrape <img> and CSS background-image with Playwright."""
    try:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=20000)

        srcs = []

        # 1. Normal <img>
        imgs = await page.query_selector_all("img")
        for img in imgs:
            src = await img.get_attribute("src")
            if src:
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = url.rstrip("/") + src
                srcs.append(src)

        # 2. Background-image
        bg_elements = await page.query_selector_all("*")
        for el in bg_elements:
            style = await el.evaluate("(e) => getComputedStyle(e).backgroundImage")
            if style and "url(" in style:
                matches = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
                for m in matches:
                    if m.startswith("//"):
                        m = "https:" + m
                    elif m.startswith("/"):
                        m = url.rstrip("/") + m
                    srcs.append(m)

        await browser.close()
        return srcs
    except Exception as e:
        print(f"⚠️ Playwright fetch failed: {e}")
        return []


def scrape_bs4_images(html, base_url):
    """Scrape <img> and CSS background-image using BeautifulSoup."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        urls = []

        # 1. Normal <img>
        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = base_url.rstrip("/") + src
                urls.append(src)

        # 2. Inline style background-image
        for div in soup.find_all(style=True):
            style = div["style"]
            if "background-image" in style:
                matches = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
                for m in matches:
                    if m.startswith("//"):
                        m = "https:" + m
                    elif m.startswith("/"):
                        m = base_url.rstrip("/") + m
                    urls.append(m)

        return urls
    except Exception as e:
        print(f"⚠️ BeautifulSoup failed: {e}")
        return []


async def duckduckgo_fallback(session, merchant, website):
    query = f"{merchant} {website}"
    search_url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"
    try:
        html = await fetch(session, search_url)
        if not html:
            return []
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.find_all("img")
        urls = [tag["src"] for tag in img_tags if tag.get("src")]
        return urls[:5]  # top 5
    except Exception as e:
        print(f"⚠️ DuckDuckGo fallback failed: {e}")
        return []


async def process_merchant(merchant, website, session, playwright, output_dir, writer, sem):
    async with sem:
        print(f"🔎 Processing {merchant} ({website})")
        banner_path = None
        source = ""

        # Step 1 → Playwright
        urls = await scrape_site_images(playwright, website)
        for url in urls:
            path = await download_and_check(url, session, output_dir, merchant)
            if path:
                banner_path = path
                source = "playwright"
                break

        # Step 2 → BeautifulSoup fallback
        if not banner_path:
            print(f"⚠️ Trying BeautifulSoup for: {merchant} {website}")
            html = await fetch(session, website)
            if html:
                urls = scrape_bs4_images(html, website)
                for url in urls:
                    path = await download_and_check(url, session, output_dir, merchant)
                    if path:
                        banner_path = path
                        source = "bs4"
                        break

        # Step 3 → DuckDuckGo fallback
        if not banner_path:
            print(f"⚠️ Trying DuckDuckGo for: {merchant} {website}")
            urls = await duckduckgo_fallback(session, merchant, website)
            for url in urls:
                path = await download_and_check(url, session, output_dir, merchant)
                if path:
                    banner_path = path
                    source = "duckduckgo"
                    break

        writer.writerow({
            "merchant_name": merchant,
            "merchant_website": website,
            "banner_image": banner_path if banner_path else "",
            "source": source if source else ""
        })


async def main(csv_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    csv_out = os.path.join(output_dir, "results.csv")

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async with aiohttp.ClientSession() as session:
        async with async_playwright() as playwright:
            with open(csv_file, newline="", encoding="utf-8") as f, \
                 open(csv_out, "w", newline="", encoding="utf-8") as fout:
                reader = csv.DictReader(f)
                fieldnames = ["merchant_name", "merchant_website", "banner_image", "source"]
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()

                tasks = [
                    process_merchant(row["merchant_name"], row["merchant_website"],
                                     session, playwright, output_dir, writer, sem)
                    for row in reader
                ]
                await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Input CSV with merchant_name, merchant_website")
    parser.add_argument("--output", required=True, help="Output directory for banners and results")
    args = parser.parse_args()

    asyncio.run(main(args.csv, args.output))
