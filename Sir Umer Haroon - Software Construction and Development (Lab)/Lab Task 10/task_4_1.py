import asyncio

import requests


async def fetch_status(delay):
    url = f"https://httpbin.org/delay/{delay}"
    response = await asyncio.to_thread(requests.get, url, timeout=10)
    response.raise_for_status()
    return response.status_code


async def main():
    task_2_seconds = asyncio.create_task(fetch_status(2))
    task_1_second = asyncio.create_task(fetch_status(1))
    print("Both tasks started")

    status_2_seconds = await task_2_seconds
    status_1_second = await task_1_second
    print(f"2-second task result: {status_2_seconds}")
    print(f"1-second task result: {status_1_second}")


if __name__ == "__main__":
    asyncio.run(main())

# Task 4.1 answer: The one-second task runs in the background while the
# two-second task is awaited, so their network waits overlap.
