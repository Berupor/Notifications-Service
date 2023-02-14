import os
import telegram
import asyncio
import git


async def send_telegram_message(api_token, chat_id, message):
    bot = telegram.Bot(token=api_token)
    await bot.send_message(chat_id=chat_id, text=message)


api_token = os.environ["TELEGRAM_API_TOKEN"]
chat_id = os.environ["CHAT_ID"]
# project_name = "Notifications service"
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

tests_successful = os.environ["TESTS"]
if tests_successful == 'Success':
    message = f'{repo}: pipeline for {sha} passed successfully'
else:
    message = f'{repo}: pipeline for {sha} failed'

asyncio.run(send_telegram_message(api_token, chat_id, message))
