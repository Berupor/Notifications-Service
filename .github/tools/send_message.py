import os
import telegram
import asyncio
import git


async def send_telegram_message(api_token, chat_id, message):
    bot = telegram.Bot(token=api_token)
    await bot.send_message(chat_id=chat_id, text=message)


api_token = os.environ["TELEGRAM_API_TOKEN"]
chat_id = os.environ["CHAT_ID"]
tests = os.environ["TESTS"]

repo = git.Repo(search_parent_directories=True)
commit_sha = repo.head.object.hexsha
repo_name = os.path.basename(repo.working_dir)

if tests == 'Success':
    message = f'{repo_name}: pipeline for ```{commit_sha}``` passed successfully.'
else:
    message = f'{repo_name}: pipeline for ```{commit_sha}``` failed.'

asyncio.run(send_telegram_message(api_token, chat_id, message))
