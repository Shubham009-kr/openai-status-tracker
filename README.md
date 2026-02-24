OpenAI Status Monitor (Event-Driven Python App)
Overview

This project is a lightweight, event-driven Python application that automatically tracks and logs service updates from the OpenAI Status Page.

The application detects new incidents, outages, or degradations related to OpenAI products (such as Chat Completions, Responses API, Images, etc.) and prints clean, readable logs to the console.

It is intentionally designed as a long-running background worker, not a web application.

Key Highlights

✅ Event-driven monitoring using OpenAI’s official Atom feed

✅ Detects new updates across restarts

✅ Avoids inefficient polling and HTML scraping

✅ Supports both local interactive mode and hosted non-interactive mode

✅ Clean console output (HTML stripped)

✅ Defensive handling of network and data edge cases

✅ Designed to scale to 100+ status providers

✅ No database, no UI, minimal dependencies

Why Atom Feed Instead of the Website?

OpenAI’s public status page:

https://status.openai.com/

is designed for human users.

This project instead uses the official machine-readable Atom feed:

https://status.openai.com/history.atom
Why this matters

Atom feeds are purpose-built for automation and monitoring

Avoids fragile HTML scraping

Naturally event-driven

Efficient and scalable

Matches real-world SRE / monitoring practices

This directly aligns with the assignment requirement to avoid manual refreshes and inefficient polling.

How It Works (High-Level Design)

Fetches the OpenAI status Atom feed

Generates a stable unique ID for the latest update

Compares it with the last seen update ID (persisted locally)

Behavior:

If a new update exists → prints the latest update

If no new update exists → prints a “No new updates” message and the last known update

In local mode, provides an option to:

View full historical logs

Exit the application

In hosted mode, runs continuously without user input

Execution Modes
1️⃣ Local Interactive Mode (Default)

Used when running locally on a developer machine.

Features:

Interactive console menu

Option to view full logs

Useful for testing and exploration

Run locally:

python main.py
2️⃣ Hosted / Non-Interactive Mode (Production)

Used when running on cloud platforms (Railway, Render, Fly.io).

Features:

No input() calls

Runs continuously as a background worker

Periodically checks for new updates

Logs output to platform log stream

Enabled via environment variable:

HOSTED_MODE=true
Project Structure
openai-status-tracker/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
Runtime State

last_seen.txt is auto-generated at runtime

Stores the last processed update ID

Not committed to Git

Requirements

Python 3.10+

Dependencies:

feedparser

Install dependencies:

pip install -r requirements.txt
Example Output
New Update Detected
🔍 OpenAI Status Monitor

✅ New update detected!

[2026-02-24 16:42:11]
Product: OpenAI API – Chat Completions
Status: Degraded performance due to upstream issue
No New Updates
ℹ️ No new updates.

Last known update:
[2026-02-24 16:42:11]
Product: OpenAI API – Chat Completions
Status: Degraded performance due to upstream issue
Deployment (Railway)

This application is deployed as a background worker on Railway.

Why Railway?

Supports long-running Python processes

Persistent filesystem

Live log streaming

Suitable for monitoring workloads

Railway Configuration

Build Command

pip install -r requirements.txt

Start Command

python main.py

Environment Variables

HOSTED_MODE=true

No web server or exposed ports are required.

Error Handling & Edge Cases Covered

Network or feed fetch failures

Empty or malformed feed responses

HTML-rich summaries cleaned for readability

Duplicate updates avoided across restarts

Cloud environments without stdin (EOFError handled)

Graceful degradation instead of crashes

Scalability

This design can easily be extended to monitor:

Multiple providers

Multiple feeds

Additional alerting mechanisms (email, Slack, etc.)

The core logic remains unchanged.

What This Project Demonstrates

Event-driven system design

Practical Python backend skills

Cloud deployment awareness

Defensive coding practices

Clear separation of concerns

Production-ready thinking without over-engineering

Future Enhancements (Optional)

Support multiple status providers

Structured logging

Alerting integrations

Configurable polling intervals

Containerized deployment

Summary

This project intentionally prioritizes:

Correctness

Clarity

Scalability

Operational realism

over unnecessary complexity.

It reflects how real monitoring and observability tools are built in production environments.

Author

Built as part of a technical assignment to demonstrate event-driven monitoring using Python.
