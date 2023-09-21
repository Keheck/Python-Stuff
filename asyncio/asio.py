import asyncio

async def say(thing: str, sec_delay: int):
    await asyncio.sleep(sec_delay)
    print(thing)

async def main():
    print("started")
    hello_task = asyncio.create_task(say("Hello", 1))
    await asyncio.sleep(2)
    await hello_task
    print("World")


asyncio.run(main())
