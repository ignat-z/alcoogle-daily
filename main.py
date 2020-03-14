from collections import Counter

from envparse import env
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotoVideo, InputMessagesFilterRoundVideo

from results_s3 import ResultsS3
from results_view import ResultsView
from results_history import ResultsHistory

env.read_envfile()

BUCKET_NAME = env("BUCKET_NAME")
CHANNEL_NAME = env("CHANNEL_NAME")
API_ID = int(env("TELEGRAM_API_ID"))
API_HASH = env("TELEGRAM_API_HASH")

client = TelegramClient('session_name', API_ID, API_HASH)
client.start()


async def chat_id():
    non_archived = await client.get_dialogs(archived=False)
    chat = next(dialog for dialog in non_archived if dialog.title == CHANNEL_NAME)
    return chat.id


async def main():
    result = Counter()
    async for message in client.iter_messages(await chat_id(), filter=InputMessagesFilterPhotoVideo):
        result[message.post_author] += 1
    async for message in client.iter_messages(await chat_id(), filter=InputMessagesFilterRoundVideo):
        result[message.post_author] += 1

    ResultsHistory().save(result)
    ResultsS3(BUCKET_NAME).upload(ResultsView().render(result))


with client:
    client.loop.run_until_complete(main())
