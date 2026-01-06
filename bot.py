# ================= IMPORTS =================
import os
import time
import feedparser
from telegram import Bot
from telegram.ext import Updater, CommandHandler


# ================= BASIC CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")   # Render ENV variable
CHANNEL_ID = "@muftdeals"            # Telegram channel username


# ================= RSS FEEDS (MULTIPLE – FAST) =================
RSS_FEEDS = [
    "https://www.dealsmagnet.com/feed"
]

# ================= TIMING =================
CHECK_INTERVAL = 120   # 2 minutes (testing ke liye fast)
POST_DELAY = 180


# ================= BOT OBJECT =================
bot = Bot(token=BOT_TOKEN)


# ================= DUPLICATE SYSTEM =================
def load_posted():
    try:
        with open("posted.txt", "r") as f:
            return set(line.strip() for line in f if line.strip())
    except:
        return set()

def save_posted(link):
    with open("posted.txt", "a") as f:
        f.write(link + "\n")

posted_links = load_posted()


# ================= TEXT CLEANER =================
def clean_text(text):
    if not text:
        return ""
    return text.replace("<br />", "").replace("&nbsp;", "").strip()[:200]


# ================= MANUAL FORCE COMMAND =================
def force(update, context):
    bot.send_message(
        chat_id=CHANNEL_ID,
        text="⚡ FORCE TEST OK — Bot live hai aur post kar sakta hai."
    )


# ================= COMMAND HANDLER SETUP =================
updater = Updater(token=BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("force", force))
updater.start_polling()


print("🤖 Bot started successfully")


# ================= MAIN AUTO POST LOOP =================
while True:
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            link = entry.link.strip()

            if link in posted_links:
                continue

            title = entry.title
            summary = clean_text(entry.get("summary", ""))

# ---- BASIC QUALITY FILTER ----
low_title = title.lower()

if "off" not in low_title and "₹" not in title and "%" not in title:
    continue
            message = (
    f"🔥 {title}\n\n"
    f"⚡ Limited Time Offer\n"
    f"🛒 Buy Now 👇\n"
    f"{link}"
)

            try:
                bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    disable_web_page_preview=False
                )

                save_posted(link)
                posted_links.add(link)
                time.sleep(POST_DELAY)

            except Exception as e:
                print("Telegram error:", e)

    time.sleep(CHECK_INTERVAL)