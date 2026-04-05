# Greenhouse Job Notifier

Automatically scrapes job postings from any Greenhouse job board, matches them to your resume using Gemini AI, and sends you a daily email with relevant roles.

## How It Works

1. **Scrape** — Fetches current job listings from a configurable Greenhouse board
2. **Filter** — Skips jobs you've already seen (tracked in `data/seen_jobs.json`)
3. **Match** — Uses Google Gemini to score each job's relevance to your resume
4. **Notify** — Sends an email summary of matched jobs with relevance scores and explanations

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- A [Google AI API key](https://aistudio.google.com/apikey) (for Gemini)
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) for sending emails

### Installation

```bash
git clone https://github.com/your-username/airbnb-job-notifier.git
cd airbnb-job-notifier
uv sync
```

### Environment Variables

Create a `.env` file in the project root:

```
GENAI_API_KEY=your_google_ai_api_key
GREENHOUSE_BOARD_TOKEN=airbnb
USER_NAME=Your Name
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com
RESUME_CONTENT=Paste your resume text here...
```

`GREENHOUSE_BOARD_TOKEN` is the company identifier in the Greenhouse URL (e.g. `airbnb`, `spotify`, `cloudflare`).

## Usage

### Run Locally

```bash
uv run main.py
```

### Automated (GitHub Actions)

The included workflow runs daily at 9:00 AM ET. To enable it:

1. Push the repo to GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Add each environment variable from above as a repository secret

The workflow automatically commits updated `seen_jobs.json` so you won't get repeat notifications.

## Project Structure

```
main.py              # Entry point — orchestrates the pipeline
src/
  scraper.py         # Fetches and filters jobs from Greenhouse API
  matcher.py         # Scores job relevance using Gemini AI
  notify.py          # Sends email alerts via Gmail SMTP
  models.py          # Pydantic data models
data/
  seen_jobs.json     # Tracks previously seen job IDs
```