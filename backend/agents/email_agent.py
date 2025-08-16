import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_email_with_attachment(name, recipient_email, pdf_data, filename):
    msg = EmailMessage()
    msg['Subject'] = f"Your Travel Itinerary from TripTacticx, {name}!"
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    msg.set_content(f"""\
Hi {name},

Thank you for using TripTacticx!

Attached is your personalized travel itinerary. Have a fantastic trip!

Best,
TripTacticx Team
""")

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=filename)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
