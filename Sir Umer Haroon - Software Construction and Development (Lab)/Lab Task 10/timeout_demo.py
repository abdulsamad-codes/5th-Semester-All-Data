import asyncio

import requests


async def slow_request():
    url = "https://httpbin.org/delay/5"
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    return response.status_code


async def main():
    try:
        print("Requesting a page that takes 5s on the server...")
        status = await asyncio.wait_for(slow_request(), timeout=2.0)
        print(f"Got status {status} (this should not print)")
    except asyncio.TimeoutError:
        print("Timed out after 2 seconds - cancelled the request.")


if __name__ == "__main__":
    asyncio.run(main())
