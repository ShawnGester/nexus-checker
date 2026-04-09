import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
load_dotenv()
APP_PASSWORD = os.getenv("NEXUS_PASSWORD")
EMAIL = os.getenv("NOTIFICATION_EMAIL")
DATE = os.getenv("MAX_DATE")
NEXUS_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=20&locationId=5020&minimum=1'
TIME_FORMAT = '%A, %B %d, %Y @ %I:%M %p'

# Function definition to execute fetching appointment slots. Originally written for AWS Lambda.
def lambda_handler(event, context):
    # Get current booked appointment time
    current_appt_time = datetime.fromisoformat(DATE)
    # Get new available appointment slots
    try:
        nexus_response = requests.get(NEXUS_URL)
        nexus_response.raise_for_status() # Raises error for 4xx or 5xx responses
        slots = nexus_response.json()
    except Exception as e:
        return {"message": f"Error fetching slots: {e}"}    

    available_slots = [datetime.fromisoformat(slot['startTimestamp']) for slot in slots if datetime.fromisoformat(slot['startTimestamp']) < current_appt_time]

    if not available_slots:
        return {"message": "No earlier slots available."}

    # Create email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Nexus Appointment Slots Available!"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    html_content = f"""
    <p>Good news! New Nexus appointment(s) available on the following dates:</p>
    <ul>
    {''.join(f'<li>{slot.strftime(TIME_FORMAT)}</li>' for slot in available_slots)}
    </ul>
    <p>Your current appointment is on {current_appt_time.strftime(TIME_FORMAT)}</p>
    <p>If this sounds good, please sign in to <a href='https://ttp.cbp.dhs.gov/'>TTP Portal</a> to reschedule.</p>
    """

    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())

    return {"message": "Notification sent."}

if __name__ == "__main__":
    # Simulate AWS Lambda trigger
    result = lambda_handler(None, None)
    print(result)