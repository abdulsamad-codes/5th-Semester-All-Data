import time

import requests
from bs4 import BeautifulSoup


URLS = [
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/page/2/",
    "https://quotes.toscrape.com/page/3/",
]


def fetch_title(url):
    print(f"START  {url}")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.text.strip()
    print(f"DONE   {url}  ->  {title[:40]}...")
    return title


start = time.perf_counter()
for url in URLS:
    fetch_title(url)
elapsed = time.perf_counter() - start
print(f"\nTotal time: {elapsed:.2f}s")

# Part 1 answers:
# 1. The START and DONE lines alternate: each START is followed by its DONE
#    before the next URL starts.
# 2. requests.get returns control only after the network response is received,
#    so it blocks the program while the request is in progress.
