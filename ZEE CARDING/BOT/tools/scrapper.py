import json
from pyrogram import Client, filters
from FUNC.defs import *
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *
from FUNC.scraperfunc import *

# Load config safely
try:
    with open("FILES/config.json", "r", encoding="utf-8") as f:
        DATA = json.load(f)
        API_ID = DATA.get("API_ID")
        API_HASH = DATA.get("API_HASH")
        if not API_ID or not API_HASH:
            raise ValueError("❌ Missing API_ID or API_HASH in config.json")
except Exception as e:
    print(f"❌ Config Load Error: {e}")
    raise SystemExit

# Scraper client
scraper = Client("Scrapper", api_id=API_ID, api_hash=API_HASH)

# Command handler template
async def handle_scrape(message, scrape_type):
    try:
        checkall = await check_all_thing(scraper, message)
        if not checkall[0]:
            return

        role = checkall[1]
        args = message.text.split()

        if scrape_type == "bin":
            if len(args) < 4:
                await message.reply_text("""<b>Wrong Format ❌</b>\n\n<code>/scrbin bin username 50</code>""")
                return
            scrape_bin, channel_link, limit = args[1], args[2], int(args[3])
        else:
            if len(args) < 3:
                await message.reply_text(f"""<b>Wrong Format ❌</b>\n\n<code>/{scrape_type} username 50</code>""")
                return
            channel_link, limit = args[1], int(args[2])
            scrape_bin = None

        # Role-based limits
        if role == "FREE" and limit > 5000 or role == "PREMIUM" and limit > 10000:
            await message.reply_text(f"""<b>Limit Reached ⚠️</b>\n\nYour plan allows up to {5000 if role == "FREE" else 10000} items.""")
            return

        await scraper.start()

        if "https" in channel_link:
            check_link = await check_invite_link(scraper, channel_link)
            if not check_link:
                await message.reply_text("<b>Wrong Invite Link ❌</b>\n\nPlease check your link and try again.")
                return

            channel_id, channel_title = check_link[1], check_link[2]
            if scrape_type == "scr":
                await cc_private_scrape(message, scraper, scraper, channel_id, channel_title, limit, role)
            elif scrape_type == "scrsk":
                await sk_private_scrape(message, scraper, scraper, channel_id, channel_title, limit, role)
            elif scrape_type == "bin":
                await bin_private_scrape(message, scraper, scraper, scrape_bin, channel_id, channel_title, limit, role)
        else:
            status_msg = await message.reply_text(f"<b>Gate: {scrape_type.upper()} Scraper ♻️</b>\n\nScraping {limit} from @{channel_link}...")
            if scrape_type == "scr":
                await cc_public_scrape(message, scraper, scraper, channel_link, limit, status_msg, role)
            elif scrape_type == "scrsk":
                await sk_public_scrape(message, scraper, scraper, channel_link, limit, status_msg, role)
            elif scrape_type == "bin":
                await bin_public_scrape(message, scraper, scraper, scrape_bin, channel_link, limit, status_msg, role)

    except Exception:
        import traceback
        await error_log(traceback.format_exc())

# Command bindings — use the actual instance name: scraper
@scraper.on_message(filters.command("scr", [".", "/"]))
async def scr_cmd(client, message):
    await handle_scrape(message, "scr")

@scraper.on_message(filters.command("scrsk", [".", "/"]))
async def scrsk_cmd(client, message):
    await handle_scrape(message, "scrsk")

@scraper.on_message(filters.command("scrbin", [".", "/"]))
async def scrbin_cmd(client, message):
    await handle_scrape(message, "bin")