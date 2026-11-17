import asyncio
import time

import requests
from bs4 import BeautifulSoup


URLS = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
]


async def fetch_title_async(url):
    print(f"START  {url}")
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.text.strip()
    print(f"DONE   {url}  ->  {title[:40]}...")
    return title


async def main():
    start = time.perf_counter()
    await fetch_title_async(URLS[0])
    print("--- between page 1 and page 2 ---")
    await fetch_title_async(URLS[1])
    await fetch_title_async(URLS[2])
    elapsed = time.perf_counter() - start
    print(f"\nTotal time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())

# Task 2.1 answer: await pauses this coroutine until its operation finishes,
# then execution continues with the next statement.
