import asyncio
import aiofiles
import datetime
import argparse
import logging
import json


async def chat_client(host, port, path):
    #4652777a-6261-11ec-8c47-0242ac110002
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        data = await reader.read(100)
        logging.info(data.decode())
        async with aiofiles.open(path, 'a') as f:
            await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")


async def send_message(host, port, path, token):
    reader, writer = await asyncio.open_connection('minechat.dvmn.org', 5050)

    if not await is_authentic_token(reader, writer, token):
        logging.info('Token is not valid')
        writer.close()
        return

    writer.write('33\n\n'.encode())
    await writer.drain()

    response = await reader.read(500)
    logging.info(response)

    logging.info('sended message')

    writer.close()


async def is_authentic_token(reader, writer, token):
    # writer.write(f'{token}\n\n'.encode())
    writer.write('4652777a-6261-11ec-8c47-0242ac110002\n\n'.encode())

    await writer.drain()
    await reader.readline()
    return not json.loads(await reader.readline()) is None


def input_token():
    print('please, input chat token')
    token = input()
    logging.info(f'inputed token: {token}')
    return token


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='program settings')
    parser.add_argument('--host', default='minechat.dvmn.org', help='chat ip')
    parser.add_argument('--port', default='5000', help='chat port')
    parser.add_argument('--history', default='chat.txt', help='path to txt file')
    args = parser.parse_args()

    token = input_token()

    asyncio.run(send_message(args.host, args.port, args.history, token))
    # asyncio.run(chat_client(args.host, args.port, args.history))
