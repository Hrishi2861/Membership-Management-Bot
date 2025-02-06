from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from pymongo import MongoClient
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
from logging import error as log_error, getLogger, info as log_info

LOGGER = getLogger(__name__)
load_dotenv('config.env', override=True)

OWNER_ID = os.environ.get('OWNER_ID', '')
if len(OWNER_ID) == 0:
    log_error("OWNER_ID variable is missing! Exiting now")
    exit(1)
else:
    OWNER_ID = int(OWNER_ID)

TELEGRAM_API = os.environ.get('TELEGRAM_API', '')
if len(TELEGRAM_API) == 0:
    log_error("TELEGRAM_API variable is missing! Exiting now")
    exit(1)
else:
    TELEGRAM_API = int(TELEGRAM_API)

TELEGRAM_HASH = os.environ.get('TELEGRAM_HASH', '')
if len(TELEGRAM_HASH) == 0:
    log_error("TELEGRAM_HASH variable is missing! Exiting now")
    exit(1)


BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if len(DATABASE_URL) == 0:
    log_error("DATABASE_URL variable is missing! Exiting now")
    exit(1)

DATABASE_NAME = "dumpinfo"
COLLECTION_NAME = "jetdump"

log_info("Creating client from BOT_TOKEN")
app = Client("bot", api_id=TELEGRAM_API, api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)
LOGGER.info(f"Jet Bot Started!")

mongo_client = MongoClient(DATABASE_URL)
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

scheduler = BackgroundScheduler()
scheduler.start()
pagination_state = {}


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    start_message = (
        "<blockquote>👋 **Welcome to the Jet Subscription Bot!**\n\n"
        "With this bot, you can:\n"
        "• Check your active subscriptions.\n"
        "• Receive notifications when subscriptions expire.</blockquote>\n\n"
        "<blockquote>Use the commands below to get started:\n"
        "• /my_subscriptions - Check your subscriptions.\n"
        "• Contact the <a href='tg://user?id=5839463933'>Owner</a> to Purchase Temporary Access to Jet-Mirror Dumps.</blockquote>\n\n"
        "<blockquote expandable>┎ <b>Plan & Prices:</b>\n"
        "┠ <b>Dumps I Provide:</b> <spoiler>Terabox, Free Leech Group NSFW/SFW, Paid Leech Group NSFW/SFW</spoiler>\n"
        "┠ <b><u>30 Days For ₹50/Dump</u></b>\n"
        "┠ <b><u>60 Days For ₹70/Dump</u></b>\n"
        "┠ <b><u>90 Days For ₹90/Dump</u></b>\n"
        "┠ <spoiler><b><u>Permanent Access For ₹150/Dump.\n┖(Permanent Means Permanent. If it gets banned will Provide New Link for Free.)</u></b></spoiler></blockquote>\n\n"
        "🤡 Time Wasters aka Gareeb Stay Away 🤡"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("☀️ ᴏᴡɴᴇʀ", url="https://t.me/rtx5069"),
                InlineKeyboardButton("🚀 ᴊᴏɪɴ", url="https://t.me/jetmirror"),
            ],
            [
                InlineKeyboardButton("💬 ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ", url="https://t.me/jetmirrorchatz")
            ]
        ]
    )
    start_pic = "/usr/src/app/assets/start_pic.jpg"

    await message.reply_photo(photo = start_pic, caption = start_message, reply_markup=buttons)

@app.on_message(filters.command("add") & filters.private)
async def add_user(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        args = message.text.split(maxsplit=3)
        if len(args) < 4:
            await message.reply("Usage: /add {user_id} {plan} {grp_name}")
            return

        user_id = int(args[1])
        plan = int(args[2])
        grp_name = args[3]

        try:
            plan = int(args[2])
            if plan <= 0:
                raise ValueError
        except ValueError:
            await message.reply("❌ Invalid number of days. Please enter a positive integer.")
            return

        user_info = await client.get_users(user_id)
        full_name = user_info.first_name
        if user_info.last_name:
            full_name += f" {user_info.last_name}"

        expiry_date = datetime.now() + timedelta(days=plan)

        existing_user = collection.find_one({"user_id": user_id})
        if existing_user:
            collection.update_one(
                {"user_id": user_id},
                {"$push": {
                    "subscriptions": {
                        "grp_name": grp_name,
                        "plan": f"{plan} days",
                        "expiry_date": expiry_date.strftime("%d-%m-%Y")
                    }
                }}
            )
        else:
            collection.insert_one({
                "user_id": user_id,
                "full_name": full_name,
                "subscriptions": [{
                    "grp_name": grp_name,
                    "plan": f"{plan} days",
                    "expiry_date": expiry_date.strftime("%d-%m-%Y")
                }]
            })

        await message.reply(f"✅ User {full_name} purchased {grp_name} for {plan} days.")
        photo_id = "/usr/src/app/assets/main_pic.jpg"
        try:
            await client.send_photo(
                user_id,
                photo = photo_id,
                caption =
                f"<blockquote>🎉 **Congratulations!**\n\n"
                f"You have Successfully Purchased **{grp_name} Dump** for **{plan} days**.\n"
                f"<u>**The <a href='tg://user?id=5839463933'>Owner</a> will Shortly Provide you the invite link.**</u></blockquote>\n\n"
                f"Thank you for your purchase! 😊"
            )
        except Exception as e:
            await message.reply(f"❌ Could not notify the user: {e}")

    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")

@app.on_message(filters.command("remove") & filters.private)
async def remove_user(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        args = message.text.split(maxsplit=2)
        if len(args) < 3:
            await message.reply("Usage: /remove {user_id} {grp_name}")
            return

        user_id = int(args[1])
        grp_name = args[2]

        user_data = collection.find_one({"user_id": user_id})
        if user_data:
            subscriptions = user_data.get("subscriptions", [])
            updated_subscriptions = [sub for sub in subscriptions if sub["grp_name"] != grp_name]

            if updated_subscriptions:
                collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"subscriptions": updated_subscriptions}}
                )
            else:
                collection.delete_one({"user_id": user_id})

            full_name = user_data["full_name"]
            await message.reply(f"✅ {full_name} has been successfully removed from {grp_name}.")
            try:
                await client.send_message(
                    user_id,
                    f"⚠️ **Notice:**\n\n"
                    f"Your subscription to **{grp_name} Dump** has been removed by the Owner.\n\n"
                    f"If you believe this was a Mistake, Please Contact the <a href='tg://user?id=5839463933'>Owner</a>."
                )
            except Exception as e:
                await message.reply(f"❌ Could not notify the user: {e}")
        else:
            await message.reply("❌ No information found for this user ID.")
    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")

@app.on_message(filters.command("info") & filters.private)
async def get_user_info(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ You are not authorized to use this command.")
        return

    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Usage: /info {user_id}")
            return

        user_id = int(args[1])
        user_data = collection.find_one({"user_id": user_id})

        if user_data:
            subscriptions = user_data.get("subscriptions", [])
            if not subscriptions:
                await message.reply("ℹ️ This user has no active subscriptions.")
                return

            info_message = (
                f"ℹ️ **User Information:**\n\n"
                f"**Name:** {user_data['full_name']}\n"
                f"**User ID:** {user_data['user_id']}\n\n"
                f"**Active Subscriptions:**\n"
            )
            for sub in subscriptions:
                expiry_date = datetime.strptime(sub["expiry_date"], "%d-%m-%Y")
                days_remaining = (expiry_date - datetime.now()).days
                info_message += (
                    f"• **Group Name:** {sub['grp_name']}\n"
                    f"  - **Plan:** {sub['plan']}\n"
                    f"  - **Expiry Date:** {sub['expiry_date']}\n"
                    f"  - **Days Remaining:** {days_remaining} days\n\n"
                )

            await message.reply(info_message)
        else:
            await message.reply("❌ No information found for this user ID.")
    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")



def check_expired_subscriptions():
    now = datetime.now().strftime("%d-%m-%Y")
    users = collection.find({"subscriptions.expiry_date": now})

    for user in users:
        updated_subscriptions = []
        for sub in user["subscriptions"]:
            if sub["expiry_date"] == now:
                try:
                    app.send_message(
                        chat_id=OWNER_ID,
                        text=(
                            f"<blockquote>⚠️ **Subscription Expired:**\n\n"
                            f"Your subscription to **{user['grp_name']} Dump** has expired as of **{user['expiry_date']}**.\n\n"
                            f"To continue, please contact the <a href='tg://user?id=5839463933'>Owner</a>.</blockquote>\n\n"
                            f"Thank you for using our service! 😊"
                        ),
                    )
                    app.send_message(
                        chat_id=user["user_id"],
                        text=(
                            f"⚠️ **Subscription Expired:**\n\n"
                            f"Your subscription to **{sub['grp_name']} Dump** has expired as of **{sub['expiry_date']}**.\n\n"
                            f"To continue, please contact the owner.\n\n"
                            f"Thank you for using our service! 😊"
                        ),
                    )
                except Exception as e:
                    print(f"Failed to notify user {user['user_id']} or owner: {e}")
            else:
                updated_subscriptions.append(sub)

        if updated_subscriptions:
            collection.update_one(
                {"user_id": user["user_id"]},
                {"$set": {"subscriptions": updated_subscriptions}}
            )
        else:
            collection.delete_one({"user_id": user["user_id"]})

@app.on_message(filters.command("all_users") & filters.private)
async def all_users(client, message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ Unauthorized.")
        return

    all_users = list(collection.find().sort("full_name", 1))
    if not all_users:
        await message.reply("❌ No users found.")
        return

    pagination_state[message.chat.id] = {"page": 0, "users": all_users}
    
    await send_user_page(client, message.chat.id, message_id=message.id)

async def send_user_page(client, chat_id, message_id=None, initial=False):
    state = pagination_state.get(chat_id, {})
    if not state:
        return

    page = state["page"]
    users = state["users"]
    page_size = 5
    total_pages = (len(users) + page_size - 1) // page_size

    if initial and message_id:
        await client.delete_messages(chat_id, message_id)

    start = page * page_size
    end = start + page_size
    paginated_users = users[start:end]

    user_message = f"ℹ️ **All Users (Page {page + 1}/{total_pages}):**\n\n"
    for user in paginated_users:
        user_message += f"• **Name:** {user['full_name']}\n  - **User ID:** {user['user_id']}\n\n"

    buttons = []
    if total_pages > 1:
        buttons = [
            InlineKeyboardButton("⫷", callback_data="prev_page"),
            InlineKeyboardButton("⫸", callback_data="next_page"),
        ]

    reply_markup = InlineKeyboardMarkup([buttons]) if buttons else None

    try:
        if "message_id" in state:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=state["message_id"],
                text=user_message,
                reply_markup=reply_markup
            )
        else:
            msg = await client.send_message(
                chat_id=chat_id,
                text=user_message,
                reply_markup=reply_markup
            )
            state["message_id"] = msg.message_id
    except Exception as e:
        print(f"Message edit failed: {e}")


@app.on_callback_query()
async def handle_pagination(client, callback_query):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.id

    state = pagination_state.get(chat_id, {})
    if not state:
        await callback_query.answer("Session expired. Run /all_users again.")
        return

    state["message_id"] = message_id

    page_size = 5
    total_pages = (len(state["users"]) + page_size - 1) // page_size
    current_page = state["page"]

    if callback_query.data == "next_page":
        state["page"] = min(current_page + 1, total_pages - 1)
    elif callback_query.data == "prev_page":
        state["page"] = max(current_page - 1, 0)

    await send_user_page(client, chat_id, message_id)
    await callback_query.answer()

@app.on_message(filters.command("my_subscriptions") & filters.private)
async def my_subscriptions(client, message):
    try:
        user_id = message.from_user.id
        user_data = collection.find_one({"user_id": user_id})

        if not user_data:
            await message.reply("❌ No subscription information found for you.")
            return

        subscriptions = user_data.get("subscriptions", [])
        if not subscriptions:
            await message.reply("ℹ️ You do not have any active subscriptions.")
            return

        info_message = (
            f"ℹ️ **Your Subscriptions:**\n\n"
            f"**Name:** {user_data['full_name']}\n"
            f"**User ID:** {user_data['user_id']}\n\n"
        )

        for sub in subscriptions:
            expiry_date = datetime.strptime(sub["expiry_date"], "%d-%m-%Y")
            days_remaining = max((expiry_date - datetime.now()).days, 0)
            info_message += (
                f"• **Group Name:** {sub['grp_name']}\n"
                f"  - **Plan:** {sub['plan']}\n"
                f"  - **Expiry Date:** {sub['expiry_date']}\n"
                f"  - **Days Remaining:** {days_remaining} days\n\n"
            )

        await message.reply(info_message)
    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")

scheduler.add_job(check_expired_subscriptions, "interval", hours=24)

if __name__ == "__main__":
    app.run()
