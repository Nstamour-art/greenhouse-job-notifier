import smtplib
from email.message import EmailMessage

def send_job_alert(matched_jobs: list, email_config: dict) -> None:
    # Retrieve credentials from GitHub Secrets
    EMAIL_ADDRESS = email_config.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = email_config.get('EMAIL_PASSWORD') # App Password, not your login
    TO_EMAIL = email_config.get('RECIPIENT_EMAIL')

    if not matched_jobs:
        print("No matches today, skipping email.")
        return

    # Create the email container
    msg = EmailMessage()
    msg['Subject'] = f"Daily Airbnb Job Match: {len(matched_jobs)} Roles Found"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    # Build the body text
    body = "Here are the relevant roles at Airbnb based on your resume:\n\n"
    
    for job in matched_jobs:
        title = job['title']
        location = job['location']['name']
        url = job['absolute_url']
        
        body += f"TITLE: {title}\n"
        body += f"LOCATION: {location}\n"
        body += f"LINK: {url}\n"
        body += f"REASON: {job['match_reason']}\n"
        body += f"RELEVANCE SCORE: {job['relevance_score']:.2f}\n"
        body += "-" * 30 + "\n\n"

    msg.set_content(body)

    # Send the email via Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not TO_EMAIL:
            print("Email credentials are not set properly. Check your GitHub Secrets.")
            return
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    
    print("Email sent successfully!")