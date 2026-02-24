import feedparser
import hashlib
from datetime import datetime
import re
import os
import sys

FEED_URL = "https://status.openai.com/history.atom"
STATE_FILE = "last_seen.txt"


def clean_html(text: str) -> str:
    if not text:
        return "No status message provided."
    text = re.sub(r"<.*?>", "", text)
    return " ".join(text.split())


def generate_id(entry) -> str:
    base = f"{entry.get('title', '')}{entry.get('updated', '')}"
    return hashlib.sha256(base.encode()).hexdigest()


def load_last_seen() -> str | None:
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip() or None
    except IOError:
        return None


def save_last_seen(update_id: str) -> None:
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
        sys.exit(1)

    if not feed.entries:
        print("ℹ️ No status data available.")
        sys.exit(0)

    return feed.entries


def show_full_logs(entries):
    print("\n📜 FULL STATUS LOGS\n")
    for entry in entries:
        print(format_log(entry))
    print("—" * 40)


def user_menu(entries):
    while True:
        print("\nOptions:")
        print("1. View full logs")
        print("2. Exit")

        choice = input("Enter choice (1/2): ").strip()

        if choice == "1":
            show_full_logs(entries)
        elif choice == "2":
            print("\n👋 Exiting. Monitoring stopped.")
            break
        else:
            print("❌ Invalid input. Please enter 1 or 2.")


def main():
    print("🔍 OpenAI Status Monitor\n")

    entries = fetch_feed()
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

    user_menu(entries)


if __name__ == "__main__":
    main()