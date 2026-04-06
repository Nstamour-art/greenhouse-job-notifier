import os
from src.matcher import match_jobs_to_user
from src.notify import send_job_alert
from src.scraper import scrape_jobs
from src.models import UserProfile

def main():
    # Step 1: Scrape jobs
    print("Scraping jobs...")
    jobs = scrape_jobs()
    print(f"Found {len(jobs)} new jobs.")

    if not jobs:
        print("No new jobs found. Exiting.")
        return

    # Step 2: Load user profile and resume from environment variables
    user_profile = UserProfile(id=1, name=os.environ.get("USER_NAME", "User"))
    resume = os.environ.get('RESUME_CONTENT')
    if not user_profile.name:
        print("Error: User name not found in environment variables.")
        raise ValueError("User name not found in environment variables.")
    
    if not resume:
        print("Error: Resume content not found in environment variables.")
        raise ValueError("Resume content not found in environment variables.")
    
    # Step 3: Match jobs to user profile and resume
    print("Matching jobs to user profile and resume...")
    matched_jobs = match_jobs_to_user(jobs, user_profile, resume)
    print(f"Matched {len(matched_jobs)} jobs with relevance scores.")
    # Step 4: Send email notification with matched jobs
    print("Sending email notification...")
    send_job_alert(matched_jobs, user=user_profile, email_config={
        "EMAIL_ADDRESS": os.environ.get('EMAIL_ADDRESS'),
        "EMAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD'),
        "RECIPIENT_EMAIL": os.environ.get('RECIPIENT_EMAIL'),
        "ENV_NAME": os.environ.get('ENV_NAME', 'default'),
        "GREENHOUSE_BOARD_TOKEN": os.environ.get('GREENHOUSE_BOARD_TOKEN', 'greenhouse'),
    })


if __name__ == "__main__":
    
    main()
