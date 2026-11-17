import asyncio
import time

import requests
from bs4 import BeautifulSoup


URLS = [f"https://quotes.toscrape.com/page/{page}/" for page in range(1, 6)]


async def fetch_title(url):
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.title.text.strip()


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(fetch_title(url) for url in URLS))

    print("Page titles (input order):")
    for page, title in enumerate(results, start=1):
        print(f"  Page {page}: {title}")
    print(f"Total time: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
