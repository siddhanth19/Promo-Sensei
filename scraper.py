import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, parse_qs, unquote
import json

def extract_true_url(tracking_url):
    """
    Extracts the true destination URL from a tracking URL like GrabOn's.
    """
    if not tracking_url:
        return None

    parsed_tracking_url = urlparse(tracking_url)
    query_params = parse_qs(parsed_tracking_url.query)
    if 'url' in query_params:
        encoded_destination_url = query_params['url'][0]
        true_url = unquote(encoded_destination_url)
        return true_url
    else:
        return tracking_url


async def scrape_grabon_deals_playwright():
    deals = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # Set headless=False to see the browser
        page = await browser.new_page()
        await page.goto("https://www.grabon.in/deals/", wait_until="domcontentloaded")

        await page.wait_for_selector(".g-deal", timeout=10000)

        deal_elements = await page.locator(".g-deal").all()

        for deal_element in deal_elements:
            try:
                deal_title = await deal_element.get_attribute("data-dealtitle")
                deal_url = await deal_element.get_attribute("data-dealurl")
                after_price = await deal_element.get_attribute("data-afterprice")
                merchant_name = await deal_element.get_attribute("data-dmname")
                discount_percentage_element = await deal_element.locator("span").first.all_text_contents()
                discount_percentage = discount_percentage_element[0].strip() if discount_percentage_element else "N/A"

                if deal_title is not None:
                    true_url=extract_true_url(deal_url)
                    deal = {
                        "title": deal_title,
                        "discount": discount_percentage,
                        "description": deal_title,
                        "deal_url": true_url,
                        "brand_merchant": merchant_name,
                        "price": float(after_price) if after_price else None
                    }
                    deals.append(deal)
            except Exception as e:
                pass

        await browser.close()
    return deals

def get_deals():
    extracted_deals = asyncio.run(scrape_grabon_deals_playwright())
    with open('offers.json','w') as f:
        json.dump(extracted_deals,f,indent=2)
    return extracted_deals

if __name__ == "__main__":
    get_deals()
