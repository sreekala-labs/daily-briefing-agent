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
    print(f"--Agent is searching for : {query}")
    search = DDGS().text(query, max_results=3)
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
    messages = [{
        "role": "system",
        "content": "You are a Senior Support Engineer. Your goal is to research a topic and find technical 'gotchas', API limitations, or common support issues. First, search for the topic. Then, summarize the findings for a developer."
    },
    {
        "role": "user",
        "content": f"Research the latest updates on: {topic}"
    }]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    tool_call = response.choices[0].message.tool_calls[0]
    search_results = search_web(json.loads(tool_call.function.arguments)["query"])
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": search_results
    })
    
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    return f"--- Final Support Briefing ---\nTopic: {topic}\n{final_response.choices[0].message.content}"

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
        print(f"Email sent! Message ID: {response['messageId']}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Get current month and year
current_month_year = datetime.now().strftime("%B %Y")

# List of topics for the briefing
topics = [
    f"Tech News {current_month_year}",
    f"AI News {current_month_year}",
    f"World News {current_month_year}",
    f"Cricket News {current_month_year}",
    f"Finance News {current_month_year}",
    f"Stock Market News {current_month_year}",
    f"Puzzle of the Day from Google",
    f"Word of the Day from NYT",
    f"Anything new in Software Industry {current_month_year}",
    f"System Design {current_month_year}"
]

# Collect all briefings
briefings = []
for topic in topics:
    briefings.append(run_support_brief(topic))

# Combine all briefings and send email
email_body = "\n\n".join(briefings)
send_email("Daily Morning Brief", email_body)
