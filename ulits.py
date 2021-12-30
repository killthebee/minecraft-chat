import os
import argparse
import asyncio

from contextlib import asynccontextmanager
from pathlib import Path


def get_args():
    """
    default value is suitable only for message sender, thus won't work in message reader
    file_path: might be either file with token for message sender or file with chat logs for reader
    :return: arguments
    """
    parser = argparse.ArgumentParser(description='program settings')
    parser.add_argument('--host', default='minechat.dvmn.org', help='chat ip')
    parser.add_argument('--port', default='5050', help='chat port')
    parser.add_argument('--file_path', default='chat.txt', help='path to txt file')
    args = parser.parse_args()
    os.environ["token_file_path"] = args.file_path
    return args


def save_token(token):
    with open(f'{os.environ["token_file_path"]}', 'w') as f:
        f.write(token)


def is_token_file_exists():
    token_file = Path(f'{os.environ["token_file_path"]}')
    return token_file.is_file()


def read_token_file():
    if not is_token_file_exists():
        return None
    with open(f'{os.environ["token_file_path"]}') as token_file:
        return token_file.read()


def delete_token_file():
    if not is_token_file_exists():
        return None
    os.remove(f'{os.environ["token_file_path"]}')


@asynccontextmanager
async def connect_to_chat(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        yield reader, writer
    finally:
        writer.close()
