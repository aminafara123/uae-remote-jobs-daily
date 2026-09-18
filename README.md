# UAE Remote Jobs Daily

A living dataset of remote and UAE-workable job postings in IT operations, GRC/compliance, cloud, and AI automation, collected every day by my [job-scan-automation](https://github.com/aminafara123/job-scan-automation) pipeline.

Each morning (at a randomized time between 08:00 and 12:00 UAE) the pipeline publishes its latest scan here automatically: roughly 2,200 postings pulled from eight public APIs and feeds, filtered to relevant lanes, location-triaged, and deduplicated against everything already seen. **Commits in this repository are made by that automation**, via `publish_daily.py`, which is the whole point: this repo is the pipeline's public heartbeat.

<!-- CHECKED -->Last automated check: 2026-09-18 08:45 UAE<!-- /CHECKED -->

## Why this exists

Job boards show you a moment; a dataset shows you the market. Thirty days of daily reports reveal which postings are fresh, which linger, how fast the good ones close, and how thin the genuinely UAE-eligible remote market really is once you strip the postings that say "Remote" but mean "Remote (US only)".

## Reading a report

Each daily file lists the postings that passed three gates that day: lane keywords (GRC/compliance, IT administration, cloud, AI automation), an exclusion list (off-lane roles, nationality-restricted postings, known ghost-posting patterns), and location triage, where every posting is tagged eligible, verify, or unknown, because location claims on job boards are claims, not facts.

## Recent scans

<!-- INDEX -->
| Date | Relevant postings | New that day | Link |
|---|---|---|---|
| 2026-09-17 | 75 | 7 | [report](reports/2026-09-17.md) |
| 2026-09-16 | 79 | 2 | [report](reports/2026-09-16.md) |
<!-- /INDEX -->

## About

Built and operated by Al Amin Bashir Afara, Dubai: [github.com/aminafara123](https://github.com/aminafara123) · [linkedin.com/in/aminafara](https://www.linkedin.com/in/aminafara). Post data comes from public APIs and feeds accessed politely (honest User-Agent, rate limits, no login automation). Listings belong to their respective posters.
