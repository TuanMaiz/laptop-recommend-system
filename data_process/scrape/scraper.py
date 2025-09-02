#!/usr/bin/env python3
"""
SAZO.vn Laptop Scraper
Scrapes laptop product details from SAZO.vn category pages with pagination support.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SAZOLaptopScraper:
    def __init__(self):
        self.base_url = "https://sazo.vn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        # Remove extra whitespace and normalize
        text = re.sub(r"\s+", " ", text.strip())
        return text

    def extract_brand_from_breadcrumb(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract brand from the breadcrumb structure.
        Typically the brand appears as the second item in the breadcrumb list. For example:
        <li itemprop="itemListElement">
            <a href="https://sazo.vn/product-categories/lenovo">
                <span>Lenovo</span>
            </a>
        </li>
        """
        breadcrumb_items = soup.select(
            "ul[itemtype='http://schema.org/BreadcrumbList'] li[itemprop='itemListElement']"
        )
        # Ensure we have at least 2 breadcrumb items (0: Trang chủ, 1: brand, ...)
        if len(breadcrumb_items) > 1:
            brand_item = breadcrumb_items[1].select_one("a span")
            if brand_item:
                brand_text = self.clean_text(brand_item.get_text())
                return brand_text
        return None

    def extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract price from various possible selectors"""
        price_selectors = [
            "meta[itemprop='price']",
            ".price-current",
            ".product-price",
            ".price",
            "[data-price]",
            ".current-price",
        ]

        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                if price_elem.name == "meta":
                    return price_elem.get("content")
                else:
                    price_text = self.clean_text(price_elem.get_text())
                    if price_text:
                        return price_text
        return None

    def extract_image_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main product image URL"""
        image_selectors = [
            "img.lg-image",
            ".product-image img",
            ".main-image img",
            ".product-gallery img",
            "img[itemprop='image']",
            "div.picture a img",
        ]

        for selector in image_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                img_src = img_elem.get("src") or img_elem.get("data-src")
                if img_src:
                    return urljoin(self.base_url, img_src)
        return None

    def extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product description from various possible locations"""
        desc_selectors = [
            "div.product-overview",
            ".product-description",
            ".product-detail",
            ".product-content",
            "[itemprop='description']",
            ".description",
        ]

        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                desc_text = self.clean_text(desc_elem.get_text())
                if desc_text and len(desc_text) > 10:  # Ensure meaningful content
                    return desc_text
        return None

    def extract_specifications(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract product specifications from SAZO's table format"""
        specs = {}

        # Look for the specific SAZO specification table
        spec_table = soup.select_one("table.data-table")

        if spec_table:
            # Extract from SAZO's specific table format
            spec_rows = spec_table.select("tr")
            for row in spec_rows:
                # Skip header rows
                if row.select_one(".spec-header") or row.select_one(".spec-group-name"):
                    continue

                # Extract spec name and value
                spec_name_elem = row.select_one(".spec-name")
                spec_value_elem = row.select_one(".spec-value")

                if spec_name_elem and spec_value_elem:
                    # Clean the spec name (remove HTML tags and colons)
                    spec_name = self.clean_text(spec_name_elem.get_text())
                    spec_name = spec_name.replace(":", "").strip()

                    # Clean the spec value (preserve line breaks as separators)
                    spec_value_html = str(spec_value_elem)
                    # Replace <br> tags with comma-space for better readability
                    spec_value_html = spec_value_html.replace("<br>", ", ").replace(
                        "<br/>", ", "
                    )
                    spec_value_soup = BeautifulSoup(spec_value_html, "html.parser")
                    spec_value = self.clean_text(spec_value_soup.get_text())

                    if spec_name and spec_value:
                        specs[spec_name] = spec_value

        # Fallback to other common specification formats if SAZO table not found
        if not specs:
            fallback_selectors = [
                ".product-specs table tr",
                ".specifications table tr",
                ".spec-list li",
                ".product-attributes li",
                ".technical-specs tr",
            ]

            for selector in fallback_selectors:
                spec_items = soup.select(selector)
                for item in spec_items:
                    # Try to extract key-value pairs from table rows
                    tds = item.select("td")
                    if len(tds) >= 2:
                        key = (
                            self.clean_text(tds[0].get_text()).replace(":", "").strip()
                        )
                        value = self.clean_text(tds[1].get_text())
                        if key and value and len(key) < 50:  # Reasonable key length
                            specs[key] = value
                    else:
                        # Try to extract from text with colon separator
                        text = self.clean_text(item.get_text())
                        if ":" in text and len(text) < 200:  # Reasonable length
                            key, value = text.split(":", 1)
                            key = key.strip()
                            value = value.strip()
                            if key and value and len(key) < 50:
                                specs[key] = value

        return specs

    def parse_product_page(self, url: str) -> Dict:
        """Parse individual product page and extract all relevant information"""
        try:
            logger.info(f"Scraping product: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            title_selectors = [
                "h1.product-name",
                "h1",
                ".product-title",
                "[itemprop='name']",
            ]
            title = None
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    break

            # Extract brand from breadcrumb first
            brand = self.extract_brand_from_breadcrumb(soup)

            # Fallback to brand detection from title if breadcrumb brand wasn't found
            if not brand and title:
                # Common laptop brands
                brands = [
                    "Dell",
                    "HP",
                    "Lenovo",
                    "Asus",
                    "Acer",
                    "MSI",
                    "Apple",
                    "Surface",
                    "Thinkpad",
                ]
                for b in brands:
                    if b.lower() in title.lower():
                        brand = b
                        break

            # Extract other fields
            price = self.extract_price(soup)
            description = self.extract_description(soup)
            image_url = self.extract_image_url(soup)
            specifications = self.extract_specifications(soup)

            return {
                "url": url,
                "title": title,
                "price": price,
                "description": description,
                "image_url": image_url,
                "brand": brand,
                "specifications": specifications,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return {"url": url, "error": str(e)}
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
            return {"url": url, "error": str(e)}

    def get_product_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract product links from category page"""
        link_selectors = [
            "div.product-item a[href]",
            ".product-list .product-item a",
            ".product-grid .product a",
            ".product-card a[href]",
        ]

        links = []
        for selector in link_selectors:
            elements = soup.select(selector)
            for elem in elements:
                href = elem.get("href")
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in links:
                        links.append(full_url)

        return links

    def get_next_page_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract next page URL if pagination exists"""
        next_selectors = [
            "li.next-page a",
            ".pagination .next a",
            ".pager .next a",
            "a[rel='next']",
        ]

        for selector in next_selectors:
            next_elem = soup.select_one(selector)
            if next_elem:
                href = next_elem.get("href")
                if href:
                    return urljoin(self.base_url, href)

        return None

    def crawl_category(self, start_url: str, max_pages: int = None) -> List[Dict]:
        """Crawl a category with pagination support"""
        all_products = []
        current_url = start_url
        page_count = 0

        while current_url:
            page_count += 1
            logger.info(f"Crawling page {page_count}: {current_url}")

            if max_pages and page_count > max_pages:
                logger.info(f"Reached maximum pages limit ({max_pages})")
                break

            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Get product links from current page
                product_links = self.get_product_links(soup)
                logger.info(f"Found {len(product_links)} products on page {page_count}")

                # Process each product
                for product_url in product_links:
                    product_data = self.parse_product_page(product_url)
                    all_products.append(product_data)

                    # Be polite - delay between requests
                    time.sleep(1)

                # Check for next page
                current_url = self.get_next_page_url(soup)
                if current_url:
                    logger.info(f"Next page found: {current_url}")
                    time.sleep(2)  # Longer delay between pages
                else:
                    logger.info("No more pages found")

            except requests.RequestException as e:
                logger.error(f"Error crawling page {current_url}: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error on page {current_url}: {e}")
                break

        return all_products

    def save_to_json(self, data: List[Dict], filename: str = "sazo_laptops.json"):
        """Save scraped data to JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filename}")

    def save_to_csv(self, data: List[Dict], filename: str = "sazo_laptops.csv"):
        """Save scraped data to CSV file with better specification handling"""
        if not data:
            return

        # Flatten specifications for CSV
        flattened_data = []
        for item in data:
            flat_item = item.copy()
            if "specifications" in flat_item and isinstance(
                flat_item["specifications"], dict
            ):
                specs = flat_item.pop("specifications")
                for key, value in specs.items():
                    # Clean key for CSV column name
                    clean_key = re.sub(r"[^\w\s-]", "", key).strip().replace(" ", "_")
                    flat_item[f"spec_{clean_key}"] = value
            flattened_data.append(flat_item)

        # Get all unique keys for CSV headers
        all_keys = set()
        for item in flattened_data:
            all_keys.update(item.keys())

        # Sort keys to have main fields first, then specifications
        main_fields = [
            "url",
            "title",
            "price",
            "brand",
            "description",
            "image_url",
            "scraped_at",
            "error",
        ]
        spec_fields = sorted([k for k in all_keys if k.startswith("spec_")])
        other_fields = sorted(
            [k for k in all_keys if k not in main_fields and not k.startswith("spec_")]
        )

        ordered_keys = (
            [k for k in main_fields if k in all_keys] + other_fields + spec_fields
        )

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ordered_keys)
            writer.writeheader()
            writer.writerows(flattened_data)

        logger.info(f"Data saved to {filename}")

        # Print specification summary
        spec_columns = [k for k in ordered_keys if k.startswith("spec_")]
        if spec_columns:
            logger.info(
                f"Extracted {len(spec_columns)} specification fields: {', '.join([k.replace('spec_', '') for k in spec_columns[:5]])}{'...' if len(spec_columns) > 5 else ''}"
            )


def main():
    """Main execution function"""
    scraper = SAZOLaptopScraper()

    # Example category URLs - you can modify these
    categories = [
        "https://sazo.vn/product-categories/lenovo",
        # Add more categories as needed:
        # "https://sazo.vn/product-categories/dell",
        "https://sazo.vn/product-categories/hp",
        "https://sazo.vn/product-categories/khac",
    ]

    all_data = []

    for category_url in categories:
        logger.info(f"Starting to scrape category: {category_url}")

        # You can set max_pages to limit scraping for testing
        category_data = scraper.crawl_category(
            category_url, max_pages=5
        )  # Remove max_pages for full scrape
        all_data.extend(category_data)

        logger.info(f"Scraped {len(category_data)} products from {category_url}")

        # Delay between categories
        time.sleep(3)

    # Save results
    if all_data:
        scraper.save_to_json(all_data, "sazo_laptops_enriched.json")
        # scraper.save_to_csv(all_data, "sazo_laptops.csv")

        # Print summary
        successful_scrapes = [item for item in all_data if "error" not in item]
        failed_scrapes = [item for item in all_data if "error" in item]

        print(f"\n{'='*50}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*50}")
        print(f"Total products found: {len(all_data)}")
        print(f"Successfully scraped: {len(successful_scrapes)}")
        print(f"Failed to scrape: {len(failed_scrapes)}")

        if successful_scrapes:
            print(f"\nSample of scraped data:")
            sample = successful_scrapes[0]
            for key, value in sample.items():
                if key == "specifications" and isinstance(value, dict):
                    print(f"  {key}: {len(value)} specifications found")
                    # Show first few specs as example
                    for i, (spec_key, spec_value) in enumerate(list(value.items())[:3]):
                        print(f"    - {spec_key}: {spec_value}")
                    if len(value) > 3:
                        print(f"    - ... and {len(value) - 3} more")
                elif key != "specifications":
                    display_value = (
                        str(value)[:100] + "..." if len(str(value)) > 100 else value
                    )
                    print(f"  {key}: {display_value}")

        print(f"\nOutput files:")
        print(f"  - sazo_laptops.json")
        # print(f"  - sazo_laptops.csv")
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    main()
