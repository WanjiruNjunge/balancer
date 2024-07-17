import asyncio
import aiohttp
import time
import random

async def send_request(session, url):
    path = random.choice(["/heartbeat", "/home"])  # Randomly choose a path
    full_url = f"{url}{path}"
    try:
        async with session.get(full_url, timeout=None) as response:
            status = response.status
            if status == 200:
                print(f"Success: {full_url} - Status: {status}")
            else:
                print(f"Failure: {full_url} - Status: {status}")
    except aiohttp.ClientError as e:
        print(f"Error: {full_url} - Exception: {e}")

async def main():
    url = "http://localhost:7432"  # Replace with the actual IP/hostname if needed
    num_requests = 10000
    tasks = []

    async with aiohttp.ClientSession() as session:
        for _ in range(num_requests):
            task = asyncio.ensure_future(send_request(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()

    print(f"\nSent 10000 requests in {end_time - start_time:.2f} seconds")
