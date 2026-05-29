import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI
from dotenv import load_dotenv
from ddgs import DDGS
from datetime import datetime
from sib_api_v3_sdk import Configuration, ApiClient, SendSmtpEmail
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi

load_dotenv()
client = OpenAI()

def search_web(query):
    print(f"--Agent is searching for: {query}")
    search = DDGS().text(f"latest {query}", max_results=3)  # Add "latest" to the query
    return json.dumps(search)
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet for technical documentation or news",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant information",
                        "required": ["query"]
                    }
                }
            }
        }
    }
]

def run_support_brief(topic):
    # Use DDG search directly for the topic
    print(f"Generating briefing for: {topic}")
    try:
        search_results = search_web(topic)  # Fetch search results from DDG
        results = json.loads(search_results)  # Parse the JSON response
        # Format the results into a readable summary
        summary = "\n".join([f"- {result['title']}: {result['href']}" for result in results[:3]])
        return f"--- Support Briefing ---\nTopic: {topic}\n{summary}"
    except Exception as e:
        return f"--- Support Briefing ---\nTopic: {topic}\nError fetching data: {e}"

def send_email(subject, body):
    brevo_api_key = os.getenv("BREVO_API_KEY")
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")

    # Configure Brevo API client
    configuration = Configuration()
    configuration.api_key['api-key'] = brevo_api_key

    # Create the email
    email = SendSmtpEmail(
        sender={"email": sender_email},
        to=[{"email": receiver_email}],
        subject=subject,
        html_content=f"<html><body><p>{body.replace('\n', '<br>')}</p></body></html>"
    )

    # Send the email
    api_client = ApiClient(configuration)
    api_instance = TransactionalEmailsApi(api_client)
    try:
        response = api_instance.send_transac_email(email)
        # Print the response object to inspect its attributes
        print(f"Email sent successfully! Response: {response}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Get current month and year
current_day_month_year = datetime.now().strftime("%B %d, %Y")

# List of topics for the briefing
topics = [
    f"Tech News {current_day_month_year}",
    f"AI News {current_day_month_year}",
    f"World News {current_day_month_year}",
    f"Cricket News {current_day_month_year}",
    f"Finance News {current_day_month_year}",
    f"Stock Market News {current_day_month_year}",
    f"Puzzle of the Day from Google",
    f"Word of the Day from NYT",
    f"Anything new in Software Industry {current_day_month_year}",
    f"System Design {current_day_month_year}"
]

# Collect all briefings
briefings = []
for topic in topics:
    briefings.append(run_support_brief(topic))  # Use DDG search for each topic

# Combine all briefings and send email
email_body = "\n\n".join(briefings)
send_email("Daily Morning Brief", email_body)
