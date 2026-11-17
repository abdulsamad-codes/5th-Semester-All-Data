import asyncio
import time


async def cpu_work(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


async def main():
    start = time.perf_counter()
    results = await asyncio.gather(
        cpu_work(10_000_000),
        cpu_work(10_000_000),
    )
    elapsed = time.perf_counter() - start
    print(f"Two CPU-heavy coroutines: {elapsed:.2f}s")
    print("They ran one after another in the same thread - async did not parallelize them.")
    return results


if __name__ == "__main__":
    asyncio.run(main())
