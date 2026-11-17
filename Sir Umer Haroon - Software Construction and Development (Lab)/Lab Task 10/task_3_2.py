import asyncio
import time

import requests
from bs4 import BeautifulSoup


URLS = [
    "https://quotes.toscrape.com/page/1/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
    "https://quotes.toscrape.com/page/4/",
    "https://quotes.toscrape.com/",
]


async def fetch_title(url):
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.title.text.strip()


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(fetch_title(url) for url in URLS))

    print("Page titles (input order):")
    for url, title in zip(URLS, results):
        print(f"  {url}: {title}")
    print(f"Total time: {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())

# Task 3.2 answer: asyncio.gather returns results in the order of the input
# coroutines, even when a later request completes first.
