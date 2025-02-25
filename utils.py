import asyncio


async def dot_animation():
    while True:
        for dots in range(1, 4):
            print(f"\r🤖 Processing bookmarks{'.' * dots}", end="")
            await asyncio.sleep(0.5)
        print("\r", end="")
