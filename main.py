import json
from datetime import datetime

import boto3
from envparse import env
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotoVideo

from results_view import ResultsView

env.read_envfile()

BUCKET_NAME = env("BUCKET_NAME")
CHANNEL_NAME = env("CHANNEL_NAME")
API_ID = int(env("TELEGRAM_API_ID"))
API_HASH = env("TELEGRAM_API_HASH")
SOURCE_FILENAME = 'index.html'
TODAY = datetime.now().strftime('%Y-%m-%d')

client = TelegramClient('session_name', API_ID, API_HASH)
client.start()


def write_stats(result):
    filename = TODAY + ".json"
    current = open(filename, "w")
    current.write(json.dumps(result))
    current.close()


async def main():
    result = {}
    non_archived = await client.get_dialogs(archived=False)
    chat = next(dialog for dialog in non_archived if dialog.title == CHANNEL_NAME)
    async for message in client.iter_messages(chat.id, filter=InputMessagesFilterPhotoVideo):
        if message.post_author not in result:
            result[message.post_author] = 0
        else:
            result[message.post_author] += 1

    write_stats(result)

    index = open(SOURCE_FILENAME, "w")
    index.write(ResultsView().render(result))
    index.close()

    S3 = boto3.client('s3')
    S3.upload_file(SOURCE_FILENAME, BUCKET_NAME, SOURCE_FILENAME, ExtraArgs={'ContentType': 'text/html'})


with client:
    client.loop.run_until_complete(main())
