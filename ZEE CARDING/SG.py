import json
from pyrogram import Client

with open("FILES/config.json", "r",encoding="utf-8") as f:
    DATA         = json.load(f)
    API_ID       = DATA["23814021"]
    API_HASH     = DATA["20ee8fa1bb2d8ba536f2082a2727ddd7"]
    BOT_TOKEN    = DATA["7869745797:AAHYApNrDAe1uMJlGEGfx6_tJI3VARdGUCA"]
    PHONE_NUMBER = DATA["+919034418800"]

user = Client("Scrapper",
              api_id       = API_ID,
              api_hash     = API_HASH ,
              phone_number = PHONE_NUMBER
              )

user.start()


