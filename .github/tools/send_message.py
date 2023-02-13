import os
import telegram
import asyncio


async def send_telegram_message(api_token, chat_id, message):
    bot = telegram.Bot(token=api_token)
    await bot.send_message(chat_id=chat_id, text=message)


api_token = os.environ["TELEGRAM_API_TOKEN"]
chat_id = os.environ["CHAT_ID"]

if "CI_SUCCESS" in os.environ:
    commit_hash = os.environ["CI_COMMIT_HASH"]
    project_name = os.environ["CI_PROJECT_NAME"]
    step_name = os.environ.get("CI_STEP_NAME")
    result = "successfully" if os.environ["CI_SUCCESS"] == "true" else "with error"
    message = f"{project_name}: Pipeline for {commit_hash} finished {result}!"
    if step_name:
        message += f"\n{step_name} failed"
else:
    message = "CI tests"

asyncio.run(send_telegram_message(api_token, chat_id, message))
