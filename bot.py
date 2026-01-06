import feedparser
import time
import requests
from telegram import Bot

# ========== CONFIG ==========
BOT_TOKEN = "8107176078:AAGNryRxC-y_UlNfpXiJk9hjAmJDoN13h3o"
CHANNEL_ID = "@muftdeals"

RSS_FEEDS = [
    "https://www.desidime.com/deals/feed"
]

CHECK_INTERVAL = 600        # 10 min
POST_DELAY = 20             # spam safe
AFFILIATE_TAG = "?affid=YOURTAG"   # placeholder

bot = Bot(token=BOT_TOKEN)

# ========== DUPLICATE SYSTEM ==========
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

# ========== IMAGE FETCH ==========
def extract_image(entry):
    if "media_content" in entry:
        return entry.media_content[0]["url"]
    return None

# ========== CLEAN TEXT ==========
def clean_text(text):
    return text.replace("<br />", "").replace("&nbsp;", "")[:200]

# ========== MAIN LOOP ==========
while True:
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            link = entry.link.strip()

            if link in posted_links:
                continue

            title = entry.title
            summary = clean_text(entry.summary)
            image_url = extract_image(entry)

            affiliate_link = link + AFFILIATE_TAG

            caption = (
                f"🔥 {title}\n\n"
                f"📝 {summary}\n\n"
                f"🛒 Buy Now 👇\n"
                f"{affiliate_link}"
            )

            try:
                bot.send_message(
    chat_id=CHANNEL_ID,
    text=caption
)

                save_posted(link)
                posted_links.add(link)
                time.sleep(POST_DELAY)

            except Exception as e:
                print("Error:", e)

    time.sleep(CHECK_INTERVAL)