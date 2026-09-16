#!/usr/bin/env python3
"""Publish the newest job-scan report into this dataset repo and push it.

Runs unattended every morning (Windows Task Scheduler -> WSL). With
--wait-random it first sleeps a random 0-230 minutes (seeded by the date),
so the daily update lands somewhere between 08:00 and roughly 12:00 UAE time.

The commit is honest about what it is: an automated daily publish. When the
scan produced nothing new, the commit updates the "last checked" line only.
"""

import datetime as dt
import random
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
SOURCE_DIR = Path.home() / "aiProjects/aminWork/job-research/scraper"
README = REPO / "README.md"
REPORTS = REPO / "reports"

# Lines in the private reports that are personal notes, not market data.
STRIP_PREFIXES = ("Floor reminder", "Reminder:")


def newest_report():
    files = sorted(SOURCE_DIR.glob("jobs-report-*.md"))
    return files[-1] if files else None


def sanitize(text):
    lines = [l for l in text.splitlines()
             if not any(l.strip().startswith(p) for p in STRIP_PREFIXES)]
    return "\n".join(lines).strip() + "\n"


def stats(text):
    m = re.search(r"Kept (\d+) on-lane.*?\*\*(\d+) new", text, re.S)
    return (m.group(1), m.group(2)) if m else ("?", "?")


def rebuild_index():
    rows = []
    for f in sorted(REPORTS.glob("*.md"), reverse=True)[:30]:
        kept, new = stats(f.read_text(encoding="utf-8"))
        rows.append(f"| {f.stem} | {kept} | {new} | [report](reports/{f.name}) |")
    table = ("| Date | Relevant postings | New that day | Link |\n"
             "|---|---|---|---|\n" + "\n".join(rows))
    text = README.read_text(encoding="utf-8")
    text = re.sub(r"(<!-- INDEX -->).*(<!-- /INDEX -->)",
                  r"\1\n" + table + r"\n\2", text, flags=re.S)
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M UAE")
    text = re.sub(r"(<!-- CHECKED -->).*(<!-- /CHECKED -->)",
                  rf"\1Last automated check: {stamp}\2", text)
    README.write_text(text, encoding="utf-8")


def run(*cmd):
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)


def main():
    if "--wait-random" in sys.argv:
        rng = random.Random(dt.date.today().isoformat())
        minutes = rng.randint(0, 230)
        print(f"sleeping {minutes} minutes before publishing")
        time.sleep(minutes * 60)

    src = newest_report()
    if src is None:
        print("no source report found")
        return 1
    date = src.stem.replace("jobs-report-", "")
    dest = REPORTS / f"{date}.md"
    body = sanitize(src.read_text(encoding="utf-8"))
    changed = not dest.exists() or dest.read_text(encoding="utf-8") != body
    if changed:
        dest.write_text(body, encoding="utf-8")
    rebuild_index()

    run("git", "add", "-A")
    if changed:
        msg = f"Automated daily scan: {date}"
    else:
        msg = f"Automated daily check: no changes ({dt.date.today().isoformat()})"
    commit = run("git", "commit", "-m", msg)
    if commit.returncode != 0:
        print("nothing to commit:", commit.stdout.strip(), commit.stderr.strip())
        return 0
    push = run("git", "push")
    print(msg, "| push:", "ok" if push.returncode == 0 else push.stderr.strip())
    return 0 if push.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
