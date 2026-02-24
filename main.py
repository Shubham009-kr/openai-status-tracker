import feedparser
import hashlib
from datetime import datetime
import re
import os
import sys
import time

FEED_URL = "https://status.openai.com/history.atom"
STATE_FILE = "last_seen.txt"

HOSTED_MODE = os.getenv("HOSTED_MODE", "false").lower() == "true"
CHECK_INTERVAL = 60


def clean_html(text: str) -> str:
    if not text:
        return "No status message provided."
    text = re.sub(r"<.*?>", "", text)
    return " ".join(text.split())


def generate_id(entry) -> str:
    base = f"{entry.get('title', '')}{entry.get('updated', '')}"
    return hashlib.sha256(base.encode()).hexdigest()


def load_last_seen():
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip() or None
    except IOError:
        return None


def save_last_seen(update_id: str):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(update_id)
    except IOError:
        print("⚠️ Warning: Could not save state.")


def format_log(entry) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = entry.get("title", "Unknown Product")
    summary = clean_html(entry.get("summary", ""))

    return (
        f"[{timestamp}]\n"
        f"Product: {title}\n"
        f"Status: {summary}\n"
    )


def fetch_feed():
    try:
        feed = feedparser.parse(FEED_URL)
    except Exception:
        print("❌ Failed to fetch status feed.")
        return []

    return feed.entries or []


def run_once():
    entries = fetch_feed()
    if not entries:
        print("ℹ️ No status data available.")
        return

    latest_entry = entries[0]
    latest_id = generate_id(latest_entry)
    last_seen_id = load_last_seen()

    if last_seen_id != latest_id:
        print("✅ New update detected!\n")
        print(format_log(latest_entry))
        save_last_seen(latest_id)
    else:
        print("ℹ️ No new updates.\n")
        print("Last known update:\n")
        print(format_log(latest_entry))


def interactive_menu(entries):
    while True:
        print("\nOptions:")
        print("1. View full logs")
        print("2. Exit")

        try:
            choice = input("Enter choice (1/2): ").strip()
        except EOFError:
            print("\n⚠️ Input not available. Exiting.")
            break

        if choice == "1":
            print("\n📜 FULL STATUS LOGS\n")
            for entry in entries:
                print(format_log(entry))
        elif choice == "2":
            print("\n👋 Exiting.")
            break
        else:
            print("❌ Invalid input.")


def main():
    print("🔍 OpenAI Status Monitor\n")

    if HOSTED_MODE:
        print("🚀 Running in HOSTED MODE (non-interactive)\n")
        while True:
            run_once()
            time.sleep(CHECK_INTERVAL)
    else:
        entries = fetch_feed()
        run_once()
        interactive_menu(entries)


if __name__ == "__main__":
    main()