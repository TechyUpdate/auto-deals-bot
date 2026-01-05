import feedparser
import time
from telegram import Bot

# ================= CONFIG =================
BOT_TOKEN = "YAHAN_APNA_BOT_TOKEN_DALO"
CHANNEL_ID = "@yourchannelusername"   # @ ke sath

RSS_FEEDS = [
    "https://www.desidime.com/deals/feed"
]

CHECK_INTERVAL = 600  # 10 minute
DELAY_BETWEEN_POSTS = 15  # seconds

bot = Bot(token=BOT_TOKEN)

# ================= DUPLICATE SYSTEM =================
def load_posted():
    try:
        with open("posted.txt", "r") as f:
            return set(f.read().splitlines())
    except:
        return set()

def save_posted(link):
    with open("posted.txt", "a") as f:
        f.write(link + "\n")

posted_links = load_posted()

# ================= MAIN LOOP =================
while True:
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            link = entry.link.strip()

            if link in posted_links:
                continue

            title = entry.title
            summary = entry.summary[:180]

            message = (
                f"🔥 {title}\n\n"
                f"📝 {summary}\n\n"
                f"🛒 Buy Now 👇\n"
                f"{link}"
            )

            try:
                bot.send_message(chat_id=CHANNEL_ID, text=message)
                save_posted(link)
                posted_links.add(link)
                time.sleep(DELAY_BETWEEN_POSTS)
            except Exception as e:
                print("Error:", e)

    time.sleep(CHECK_INTERVAL)