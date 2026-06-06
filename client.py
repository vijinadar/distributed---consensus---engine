import asyncio

transactions = [
    "TXN001",
    "TXN002",
    "TXN003",
    "TXN004",
    "TXN005"
]

async def submit_transaction(tx):

    print(f"Submitting {tx}")

    await asyncio.sleep(1)

    print(f"{tx} submitted")

async def main():

    tasks = []

    for tx in transactions:

        tasks.append(
            asyncio.create_task(
                submit_transaction(tx)
            )
        )

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())