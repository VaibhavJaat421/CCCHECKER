import json
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from pyrogram import Client, filters
import asyncio
import os

# 🔐 Replace these with your actual credentials or use environment variables
API_ID = 23814021  # your Telegram API ID
API_HASH = "20ee8fa1bb2d8ba536f2082a2727ddd7"  # your API hash
BOT_TOKEN = "7869745797:AAHgI6VVQTRLXn26M7RTzuhAAberumimgLw"  # your bot token
OWNER_ID = 8185900627  # your Telegram user ID

# 🚀 Initialize the bot
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🛑 Shutdown command
@bot.on_message(filters.command("shutdown") & filters.user(OWNER_ID))
async def shutdown_handler(client, message):
    await message.reply("🛑 Bot is shutting down...")
    await client.stop()
    os._exit(0)

# ✅ Optional: Start command
@bot.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start_handler(client, message):
    await message.reply("👋 Bot is up and running!")

# 🔄 Main async runner
async def main():
    await bot.start()
    print("✅ Bot started successfully")
    await asyncio.Event().wait()  # Keeps the bot alive

# 🔥 Launch the bot
if __name__ == "__main__":
    asyncio.run(main())
@Client.on_message(filters.command("add", [".", "/"]))
async def cmd_add(client, message):
    try:
        user_id = str(message.from_user.id)
        OWNER_ID = json.loads(open("FILES/config.json", "r", encoding="utf-8").read())["8185900627"]
        if user_id not in OWNER_ID:
            resp = (
                "<b>⛔️ Access Denied</b>\n\n"
                "<i>You do not have permission to use this command.</i>\n"
                "Please contact the bot owner @amitonmoyx for access."
            )
            await message.reply_text(resp, quote=True)
            return

        try:
            chat_id = str(message.text.split(" ")[1])
        except IndexError:
            chat_id = str(message.chat.id)

        getchat = await getchatinfo(chat_id)
        getchat = str(getchat)
        
        if getchat == "None":
            await addchat(chat_id)
            resp = (
                "<b>✅ Group Authorized</b>\n\n"
                f"<b>Group Chat ID:</b> <code>{chat_id}</code>\n\n"
                "<i>This group is now authorized to use the bot.</i>"
            )
            await message.reply_text(resp, quote=True)
            
            chat_resp = (
                "<b>✅ Authorized</b>\n\n"
                f"<b>Group Chat ID:</b> <code>{chat_id}</code>\n\n"
                "<i>This group is now authorized to use our bot. Authorized by @VAIBHAV_JAAT_OP.</i>"
            )
            try:
                await client.send_message(chat_id, chat_resp)
            except Exception:
                pass

        else:
            find = await getchatinfo(chat_id)
            find = str(find)
            if find != "None":
                resp = (
                    "<b>⚠️ Already Authorized</b>\n\n"
                    f"<b>Group Chat ID:</b> <code>{chat_id}</code>\n\n"
                    "<i>This group is already authorized to use the bot.</i>"
                )
                await message.reply_text(resp, quote=True)

    except Exception as e:
        import traceback
        await error_log(traceback.format_exc())
