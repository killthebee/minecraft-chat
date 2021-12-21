import asyncio
import aiofiles
import datetime
import argparse


async def chat_client(host, port, path):
    reader, writer = await asyncio.open_connection(host, 5000)
    while True:
        data = await reader.read(100)
        async with aiofiles.open(path, "a") as f:
            await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='program settings')
    parser.add_argument('--host', default='minechat.dvmn.org', help='chat ip')
    parser.add_argument('--port', default='5000', help='chat port')
    parser.add_argument('--history', default='chat.txt', help='path to txt file')
    args = parser.parse_args()

    asyncio.run(chat_client(args.host, args.port, args.history))
