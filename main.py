import json

from collections import ChainMap
from datetime import datetime
from envparse import env
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterPhotoVideo

import render
import boto3

SOURCE_FILENAME = 'index.html'

env.read_envfile()

BUCKET_NAME = env("BUCKET_NAME")
channel = env("CHANNEL_NAME")
api_id = int(env("TELEGRAM_API_ID"))
api_hash = env("TELEGRAM_API_HASH")

today = datetime.now().strftime('%Y-%m-%d')

client = TelegramClient('session_name', api_id, api_hash)
client.start()

def write_stats(result):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = today + ".json"
    current = open(filename, "w")
    current.write(json.dumps(result))
    current.close()

async def main():
    result = {}
    non_archived = await client.get_dialogs(archived=False)
    chat = next(dialog for dialog in non_archived if dialog.title == channel)

    async for message in client.iter_messages(chat.id, filter=InputMessagesFilterPhotoVideo):
        if not message.post_author in result: result[message.post_author] = 0
        result[message.post_author] += 1

    write_stats(result)

    index = open(SOURCE_FILENAME, "w")
    index.write(render.render(result))
    index.close()

    S3 = boto3.client('s3')
    S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME, ExtraArgs={'ContentType': 'text/html'})


with client:
    client.loop.run_until_complete(main())
