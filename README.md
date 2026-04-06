# Greenhouse Job Notifier

Automatically scrapes job postings from any Greenhouse job board, matches them to your resume using Gemini AI, and sends you a daily email with relevant roles.

## How It Works

1. **Scrape** — Fetches current job listings from a configurable Greenhouse board
2. **Filter** — Skips previously seen jobs, contract/non-full-time roles, and jobs in languages the candidate doesn't speak
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
git clone https://github.com/Nstamour-art/greenhouse-job-notifier.git
cd greenhouse-job-notifier
uv sync
```

### Environment Variables

Create a `.env` file in the project root:

```
GENAI_API_KEY=your_google_ai_api_key
GREENHOUSE_BOARD_TOKEN=job_board
ENV_NAME=default
USER_NAME=Your Name
USER_LANGUAGE=English
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com
RESUME_CONTENT=Paste your resume text here...
LOCATION_FILTER=Canada
```

| Variable | Description |
|---|---|
| `GREENHOUSE_BOARD_TOKEN` | Company identifier in the Greenhouse URL (e.g. `airbnb`, `spotify`, `cloudflare`) |
| `ENV_NAME` | Name for this configuration. Each environment gets its own `seen_jobs_{name}.json` |
| `USER_LANGUAGE` | Candidate's language(s) — jobs in other languages are filtered out by the LLM |
| `LOCATION_FILTER` | Comma-separated locations to include (also matches "remote" automatically) |

## Usage

### Run Locally

```bash
uv run main.py
```

### Automated (GitHub Actions)

The included workflow runs daily at 9:00 AM ET. To enable it:

1. Push the repo to GitHub
2. Go to **Settings → Environments** and create an environment (e.g. `default`)
3. Add each environment variable from above as a secret in that environment

#### Multiple Environments

To track multiple job boards or users, create additional GitHub environments (e.g. `spotify-jobs`) with their own secrets, then add the environment name to the matrix in [.github/workflows/daily_run.yaml](.github/workflows/daily_run.yaml):

```yaml
matrix:
  environment: [default, spotify-jobs]
```

Each environment gets its own `seen_jobs_{name}.json` file so they track independently.

The workflow automatically commits updated seen jobs files so you won't get repeat notifications.

## Project Structure

```
main.py              # Entry point — orchestrates the pipeline
src/
  scraper.py         # Fetches and filters jobs from Greenhouse API
  matcher.py         # Scores job relevance using Gemini AI
  notify.py          # Sends email alerts via Gmail SMTP
  models.py          # Pydantic data models
data/
  seen_jobs_*.json   # Tracks previously seen job IDs (per environment)
```
