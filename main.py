import asyncio
import aiofiles
import datetime
import argparse


async def chat_client(host, port, path):
    #4652777a-6261-11ec-8c47-0242ac110002
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        data = await reader.read(100)
        async with aiofiles.open(path, 'a') as f:
            await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")


async def send_message(host, port, path):
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)
    writer.write('4652777a-6261-11ec-8c47-0242ac110002\n\n'.encode())

    await writer.drain()

    writer.write('33\n\n'.encode())
    await writer.drain()

    print('2')

    writer.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='program settings')
    parser.add_argument('--host', default='minechat.dvmn.org', help='chat ip')
    parser.add_argument('--port', default='5000', help='chat port')
    parser.add_argument('--history', default='chat.txt', help='path to txt file')
    args = parser.parse_args()

    asyncio.run(send_message(args.host, args.port, args.history))
    # asyncio.run(chat_client(args.host, args.port, args.history))
