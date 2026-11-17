import asyncio
import time

import requests
from bs4 import BeautifulSoup


BASE = "https://quotes.toscrape.com/page/{}/"
PAGES = [1, 2, 3, 4, 5]


async def scrape_page(page_num):
    url = BASE.format(page_num)
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    quote = soup.find("div", class_="quote")
    if quote is None:
        raise ValueError(f"No quote found on page {page_num}")
    quote_text = quote.find("span", class_="text")
    if quote_text is None:
        raise ValueError(f"No quote text found on page {page_num}")
    return f"Page {page_num}: {quote_text.get_text(strip=True)[:60]}..."


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(scrape_page(page) for page in PAGES))
    for result in results:
        print(result)
    print(f"Total time: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
