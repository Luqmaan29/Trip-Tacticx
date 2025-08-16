from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from travel_agent import run_multi_agent
from io import BytesIO
from email.message import EmailMessage
import smtplib
import os

app = Flask(__name__, static_folder="../frontend")
CORS(app)  # Allow all origins; for production, restrict this

# Reuse your PDF generation function (adapted for Flask)
def generate_pdf(summary, agent_outputs):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.colors import HexColor, black, darkblue
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('TitleStyle', parent=styles['Title'], alignment=TA_CENTER,
                              fontSize=28, leading=34, spaceAfter=30, textColor=darkblue, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=18,
                              leading=22, spaceBefore=24, spaceAfter=14, textColor=HexColor("#004080"),
                              fontName='Helvetica-Bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle('BodyTextStyle', parent=styles['Normal'], fontSize=12,
                              leading=18, spaceAfter=8, textColor=black, alignment=TA_LEFT))

    elements = []
    elements.append(Paragraph("🌍 TripTacticx – Your Travel Plan", styles['TitleStyle']))
    elements.append(Spacer(1, 16))

    section_titles = {
        "Booking Suggestions": "🛫 Booking Suggestions",
        "Stay Options": "🏨 Stay Options",
        "Experiences": "🎨 Experiences",
        "Local Food & Dining": "🍽️ Local Food & Dining",
        "Travel Logistics": "🚗 Travel Logistics",
        "Budget Planning": "💰 Budget Planning"
    }

    def parse_content_to_flowables(text):
        flowables = []
        blocks = [b.strip() for b in text.split('\n\n') if b.strip()]
        for block in blocks:
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if all(line.startswith(('* ', '- ')) for line in lines):
                items = [line[2:].strip() for line in lines]
                list_flowable = ListFlowable(
                    [ListItem(Paragraph(item, styles['BodyTextStyle']), bulletColor=darkblue) for item in items],
                    bulletType='bullet',
                    leftIndent=20,
                    bulletFontName='Helvetica',
                    bulletFontSize=8,
                    bulletColor=darkblue,
                    start='circle',
                    spaceBefore=4,
                    spaceAfter=8,
                )
                flowables.append(list_flowable)
            else:
                paragraph_text = "<br/>".join(lines)
                flowables.append(Paragraph(paragraph_text, styles['BodyTextStyle']))
            flowables.append(Spacer(1, 6))
        return flowables

    for key, content in agent_outputs.items():
        section_title = section_titles.get(key, key)
        elements.append(Paragraph(section_title, styles['SectionHeader']))
        if content:
            elements.extend(parse_content_to_flowables(content))
        else:
            elements.append(Paragraph("No details available.", styles['BodyTextStyle']))
            elements.append(Spacer(1, 8))

    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

# Email sending function
def send_email_with_pdf(name, to_email, pdf_data):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')  # Load from .env
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials not set!")
        return False

    msg = EmailMessage()
    msg['Subject'] = f"Your TripTacticx Travel Plan, {name}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f"Hi {name},\n\nPlease find attached your personalized travel plan.\n\nSafe travels!\n\n- TripTacticx Team")

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='TripTacticx_TravelPlan.pdf')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/plan-trip', methods=['POST'])
def plan_trip():
    data = request.json
    print("Received data:", data)  # Debug

    try:
        name = data.get('name')
        email = data.get('email')

        budget_str = data['budget'].replace("Rs", "").replace(",", "").strip()
        budget = float(budget_str)

        summary, agent_outputs = run_multi_agent(
            destination=data['destination'],
            days=int(data['days']),
            group_size=int(data['group_size']),
            budget=budget,
            trip_type=data['trip_type'],
            preferences=data.get('preferences', ''),
            source_location=data['source_location']
        )

        pdf_data = generate_pdf(summary, agent_outputs)

        email_sent = send_email_with_pdf(name, email, pdf_data)

        return jsonify({
            'summary': summary,
            'agent_outputs': agent_outputs,
            'email_sent': email_sent,
            'message': "Email sent successfully!" if email_sent else "Failed to send email."
        })

    except Exception as e:
        print("Error processing request:", e)  # Debug print
        return jsonify({'error': str(e)}), 400

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
