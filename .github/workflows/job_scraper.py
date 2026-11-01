import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Target job boards or specific company pages you want to monitor
TARGET_URLS = [
    "https://news.ycombinator.com/jobs", 
]

def send_email(subject, body):
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("RECIPIENT_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not sender_email or not receiver_email or not password:
        print("Email credentials not configured. Skipping email notification.")
        return

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(body, "plain")
    message.attach(part)

    try:
        context = smtplib.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def scrape_jobs():
    print("Starting AI Product Manager job scraper...")
    all_matches = []
    
    for url in TARGET_URLS:
        try:
            response = app.scrape(url, formats=['markdown'])
            content = response.get('markdown', '')
            
            keywords = ["ai product manager", "artificial intelligence product", "technical product manager", "tpm"]
            found_matches = [kw for kw in keywords if kw in content.lower()]
            
            if found_matches:
                msg = f"Match found on {url} with keywords: {', '.join(found_matches)}"
                print(f"[MATCH FOUND] {msg}")
                all_matches.append(msg)
            else:
                print(f"No direct matches on: {url}")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # If matches were found, email them
    if all_matches:
        email_body = "Here are the job matches found today:\n\n" + "\n".join(all_matches)
        send_email("🚨 New AIPM / TPM Job Matches Found!", email_body)
    else:
        print("No new matches found today. No email sent.")

if __name__ == "__main__":
    scrape_jobs()
