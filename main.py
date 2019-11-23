import json
from datetime import datetime

from envparse import env
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotoVideo

from results_s3 import ResultsS3
from results_view import ResultsView

env.read_envfile()

CHANNEL_NAME = env("CHANNEL_NAME")
API_ID = int(env("TELEGRAM_API_ID"))
API_HASH = env("TELEGRAM_API_HASH")
BUCKET_NAME = env("BUCKET_NAME")
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
    ResultsS3(BUCKET_NAME).upload(ResultsView().render(result))


with client:
    client.loop.run_until_complete(main())
