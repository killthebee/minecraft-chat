import asyncio
import aiofiles
import datetime
import logging

from utils import get_args, connect_to_chat


async def chat_client(host, port, path):
    logging.info('Reading chat')

    async with connect_to_chat(host, port) as connection:
        reader, writer = connection
        while True:
            data = await reader.read(100)
            try:
                async with aiofiles.open(path, 'a') as f:
                    await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")
            except UnicodeDecodeError:
                logging.info(f'Failed to decode message: {data}')
                continue


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = get_args()
    asyncio.run(chat_client(args.host, args.port, args.file_path))
