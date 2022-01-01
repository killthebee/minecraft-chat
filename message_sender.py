import asyncio
import logging
import json

from utils import (get_args, connect_to_chat, save_token, read_token_file, delete_token_file, is_token_file_exists,
                   sanitize)


async def register_user(host, port):
    async with connect_to_chat(host, port) as connection:
        logging.info('Started auto registration')
        reader, writer = connection
        await reader.readline()
        writer.write('\n'.encode())
        await writer.drain()
        await reader.readline()
        username = input('enter username: ')
        writer.write(f'{sanitize(username)}\n'.encode())
        await writer.drain()
        response = await reader.readline()
        await save_token(json.loads(response)['account_hash'])
        logging.info('registered new user')


async def send_message(writer, message):
    writer.write(f'{sanitize(message)}\n\n'.encode())
    await writer.drain()


async def is_authentic_token(reader, writer, token):
    logging.info('Checking token authenticity')
    writer.write(f'{sanitize(token)}\n\n'.encode())
    await writer.drain()
    for _ in range(0, 2):
        results = await reader.readline()
    return not json.loads(results) is None


async def input_token():
    token = input('please, input chat token: ')
    logging.info('Get token from user input')
    await save_token(token)
    logging.info('Saved token file')
    return token


async def run_message_sender(host, port):
    while True:
        logging.info('Started message sender')
        if not is_token_file_exists():
            logging.info('No token file were found')
            await asyncio.sleep(0)
            continue

        async with connect_to_chat(host, port) as connection:
            logging.info('Open messenger connection')
            reader, writer = connection
            token = await read_token_file()

            if not await is_authentic_token(reader, writer, token):
                logging.info('Provided token is not authenticated')
                delete_token_file()
                continue
            logging.info('Start messaging')
            while True:
                message = input('write message: ')
                await send_message(writer, message)


async def run_token_handler(host, port):
    token_never_manually_inputted = True
    while True:
        if is_token_file_exists():
            await asyncio.sleep(1)
            continue
        logging.info('Started handling token')
        if token_never_manually_inputted:
            await input_token()
            await asyncio.sleep(0)
            token_never_manually_inputted = False
            continue
        await register_user(host, port)


async def main():
    args = get_args()
    tasks = [run_message_sender(args.host, args.port), run_token_handler(args.host, args.port)]
    await asyncio.wait(
        tasks,
        return_when=asyncio.ALL_COMPLETED
    )
    return tasks


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
