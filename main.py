import asyncio
import aiofiles
import datetime


async def chat_client():
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5000)
    while True:
        data = await reader.read(100)
        async with aiofiles.open("hmm.txt", "a") as f:
            await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")


asyncio.run(chat_client())
