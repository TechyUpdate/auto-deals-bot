import feedparser
import time
import os
from telegram import Bot

# ========== CONFIG ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")      # Render ENV variable
CHANNEL_ID = "@muftdeals"               # public channel username

RSS_FEEDS = [
    "https://www.desidime.com/deals/feed"
]

CHECK_INTERVAL = 600        # 10 minutes
POST_DELAY = 20             # anti-spam delay
AFFILIATE_TAG = "?affid=YOURTAG"

bot = Bot(token=BOT_TOKEN)


# ========== DUPLICATE SYSTEM ==========
def load_posted():
    ...
    try:
        with open("posted.txt", "r") as f:
            return set(line.strip() for line in f if line.strip())
    except:
        return set()

def save_posted(link):
    with open("posted.txt", "a") as f:
        f.write(link + "\n")

posted_links = load_posted()

# ========== IMAGE FETCH ==========
def extract_image(entry):
    if "media_content" in entry and entry.media_content:
        return entry.media_content[0].get("url")
    return None

# ========== CLEAN TEXT ==========
def clean_text(text):
    if not text:
        return ""
    return text.replace("<br />", "").replace("&nbsp;", "")[:200]

print("🤖 Bot started...")

# ========== MAIN LOOP ==========
while True:
    for feed_url in RSS_FEEDS:
        print("Checking feed:", feed_url)
        feed = feedparser.parse(feed_url)

        if not feed.entries:
            print("No entries found")
            continue

        for entry in feed.entries:
            link = entry.link.strip()

            if link in posted_links:
                continue

            title = entry.title
            summary = clean_text(entry.get("summary", ""))
            image_url = extract_image(entry)

            affiliate_link = link + AFFILIATE_TAG

            caption = (
                f"🔥 {title}\n\n"
                f"📝 {summary}\n\n"
                f"🛒 Buy Now 👇\n"
                f"{affiliate_link}"
            )

            try:
                if image_url:
                    bot.send_photo(
                        chat_id=CHANNEL_ID,
                        photo=image_url,
                        caption=caption
                    )
                else:
                    bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=caption
                    )

                save_posted(link)
                posted_links.add(link)
                print("Posted:", title)

                time.sleep(POST_DELAY)

            except Exception as e:
                print("Post failed:", e)

    print("Sleeping...")
    time.sleep(CHECK_INTERVAL)