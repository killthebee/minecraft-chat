import asyncio
import aiofiles
import datetime
import logging
import json

from asyncio import events, coroutines
from asyncio.runners import _cancel_all_tasks

from ulits import get_args, connent_to_chat, save_token, read_token_file, delete_token_file, is_token_file_exists


async def chat_client(host, port, path):
    reader, writer = await asyncio.open_connection(host, port)
    while True:
        data = await reader.read(100)
        logging.info(data.decode())
        async with aiofiles.open(path, 'a') as f:
            await f.write(f"[{datetime.datetime.now().strftime('%d.%m.%y %H:%M')}] {data.decode()}")


async def register_user(args):
    async with connent_to_chat(args.host, args.port) as connection:
        reader, writer = connection
        print('in registration')
        response = await reader.readline()
        print(response.decode())
        writer.write('\n\n'.encode())
        await writer.drain()
        response = await reader.readline()
        print(response.decode())
        #TODO meka function out of inputs
        username = input('enter username: ')
        writer.write(f'{username}\n'.encode())
        await writer.drain()
        response = await reader.readline()
        print(response.decode())
        save_token(json.loads(response)['account_hash'])
        logging.info('registered new user')


async def send_message(writer, message):

    writer.write(f'{message}\n\n'.encode())
    await writer.drain()
    logging.info('sent message')


async def is_authentic_token(reader, writer, token):
    logging.info('4')
    writer.write(f'{token}\n\n'.encode())
    await writer.drain()
    for _ in range(0, 2):
        results = await reader.readline()
    print(json.loads(results))
    return not json.loads(results) is None


def input_token():
    token = input('please, input chat token: ')
    logging.info('Get token from user input')
    save_token(token)
    return token


def get_token_from_input():
    # mb never used
    token = read_token_file()
    if not token:
        logging.info('No token file were found')
        input_token()
        return
    logging.info('Successfully get token from file')


async def run_message_sender(args):
    while True:
        logging.info('1')
        if not is_token_file_exists():
            await asyncio.sleep(0)

        async with connent_to_chat(args.host, args.port) as connection:
            logging.info('2')
            reader, writer = connection
            token = read_token_file()
            logging.info('3')

            if not await is_authentic_token(reader, writer, token):
                delete_token_file()
                logging.info('5')
                continue
            while True:
                message = input('write message: ')
                await send_message(writer, message)


async def run_token_handler(args):
    token_never_manually_inputted = True
    while True:
        if is_token_file_exists():
            await asyncio.sleep(1)
            continue
        logging.info('0')
        if token_never_manually_inputted:
            input_token()
            await asyncio.sleep(0)
            token_never_manually_inputted = False
            continue
        await register_user(args)


async def main():
    args = get_args()
    tasks = [run_message_sender(args), run_token_handler(args)]
    await asyncio.wait(
        tasks,
        return_when=asyncio.ALL_COMPLETED
    )
    return tasks


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    # for task in done:
    #     if task.cancelled():
    #         print(task, 'was cancelled')
    #     elif task.exception():
    #         print(task, 'failed with:')
    #         # we use a try/except here to reconstruct the traceback for logging purposes
    #         try:
    #             task.result()
    #         except:
    #             # we can use a bare-except as we are not trying to block
    #             # the exception -- just record all that may have happened.
    #             print('error...')
