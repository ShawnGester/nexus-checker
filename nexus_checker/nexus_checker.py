import json
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
LOCATION_IDS = [5020, 5041, 5026, 5002, 5003]  # Blaine, Vancouver Urban Enrollment Center, Vancouver Enrollment Center (Richmond)
PASTEBIN_URL = 'https://pastebin.com/raw/7FfGgXdv'
EMAIL = 'tweetumsmultiput@gmail.com'
APP_PASSWORD = 'eyop aagx eomw rcgd'
TIME_FORMAT = '%A, %B %d, %Y @ %I:%M %p'

def lambda_handler(event=None, context=None):
    # Get current booked appointment time
    pastebin_response = requests.get(PASTEBIN_URL)
    pastebin_data = pastebin_response.json()
    
    date_str = pastebin_data['date_str']
    
    # Check if the date is in ISO format or not
    try:
        # Try to parse as ISO format first
        current_appt_time = datetime.fromisoformat(date_str)
    except ValueError:
        # If ValueError, then parse it with strptime as per the original format
        current_appt_time = datetime.strptime(date_str, "%B %d, %Y %I:%M %p")

    # Collect earlier slots across all locations
    available_slots = []
    for location_id in LOCATION_IDS:
        url = f'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=20&locationId={location_id}&minimum=1'
        response = requests.get(url)
        if response.status_code != 200:
            continue
        try:
            slots = response.json()
            for slot in slots:
                slot_time = datetime.fromisoformat(slot['startTimestamp'])
                if slot_time < current_appt_time:
                    available_slots.append((location_id, slot_time))
        except ValueError:
            continue

    if not available_slots:
        return {"message": "No earlier slots available."}

    # Compose HTML email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Nexus Appointment Slots Available!"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    html_content = f"""
    <p>Good news! New Nexus appointment(s) available on the following dates and locations:</p>
    <ul>
    {''.join(f'<li>Location {loc}: {dt.strftime(TIME_FORMAT)}</li>' for loc, dt in available_slots)}
    </ul>
    <p>Your current appointment is on {current_appt_time.strftime(TIME_FORMAT)}</p>
    <p>If this sounds good, please sign in to <a href='https://ttp.cbp.dhs.gov/'>TTP Portal</a> to reschedule.</p>
    """
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())

    return {"message": "Notification sent."}

if __name__ == "__main__":
    result = lambda_handler()
    print(result)
