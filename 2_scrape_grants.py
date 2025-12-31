from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time

def scrape_grants_final(start_url):
    grants = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(start_url, timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_selector(".views-row a")

        grant_links = page.eval_on_selector_all(
            ".views-row a",
            "els => els.map(el => el.href).filter(h => h && h.includes('/funding-opportunities/startups/'))"
        )

        print(f"Found {len(grant_links)} grant links.")
        for idx, link in enumerate(grant_links):
            try:
                print(f"[{idx + 1}/{len(grant_links)}] Visiting: {link}")
                page.goto(link, timeout=60000)
                # Wait for the description container
                try:
                    page.wait_for_selector(".field-name-body", timeout=15000)
                    raw_html = page.inner_html(".field-name-body")
                except:
                    raw_html = page.content()  # fallback to full HTML if not found

                soup = BeautifulSoup(raw_html, "html.parser")
                # Extract only the main description text
                description_tag = soup.find(class_="field-name-body")
                if description_tag:
                    clean_text = description_tag.get_text(separator=" ", strip=True)
                else:
                    clean_text = soup.get_text(separator=" ", strip=True)

                title = page.title()

                grants.append({
                    "grant_title": title.strip(),
                    "grant_description": clean_text if clean_text else "Description not found."
                })

                time.sleep(0.3)

            except Exception as e:
                print(f"Error scraping {link}: {e}")
                continue


        browser.close()

    return grants

if __name__ == "__main__":
    START_URL = "https://www.indiascienceandtechnology.gov.in/funding-opportunities/startups"
    results = scrape_grants_final(START_URL)

    if results:
        with open("grants_data.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["grant_title", "grant_description"])
            writer.writeheader()
            writer.writerows(results)
        print(f"Scraped {len(results)} grants with real descriptions.")
    else:
        print("No data scraped.")
