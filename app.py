import json
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name)

# Load the JSON file containing the employee data.
with open('data.json', 'r') as f:
    employee_data = json.load(f)

# Define a function to send an email notification.
def send_email_notification(email_address, employee_name, document_type, expiry_date):
    """Sends an email notification to the specified email address.

    Args:
        email_address: The email address to send the notification to.
        employee_name: The name of the employee whose document is expiring.
        document_type: The type of document that is expiring.
        expiry_date: The expiry date of the document.
    """
    message = f"""
    Hi {employee_name},

    This is a reminder that your {document_type} will expire on {expiry_date}. Please take the necessary steps to renew your document.

    Thank you,
    Expiry Date Reminder
    """
    
    # Replace with your SendGrid API key and sender email address
    sendgrid_api_key = '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'
    sender_email = 'notifyautobot@gmail.com'

    # Send the email using SendGrid or any other email service
    requests.post(
        'https://api.sendgrid.com/v3/mail/send',
        auth=('api', sendgrid_api_key),
        headers={'Content-Type': 'application/json'},
        json={
            'personalizations': [{
                'to': [{'email': email_address}]
            }],
            'from': {'email': sender_email},
            'subject': 'Expiry Date Reminder',
            'content': [{
                'type': 'text/plain',
                'value': message
            }]
        })

# Subscribe a user to email notifications.
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email_address = data.get('email')

    if not email_address or not email_address.count('@'):
        return jsonify({'success': False, 'message': 'Invalid email address.'}), 400

    if email_address in subscribers:
        return jsonify({'success': False, 'message': 'Email address is already subscribed.'}), 200

    subscribers.append(email_address)

    # Send a confirmation email to the user.
    send_email_notification(email_address, 'Unknown', 'Subscription confirmation', 'Your subscription to email notifications was successful.')

    return jsonify({'success': True, 'message': 'Subscription successful.'}), 200

# Check and send email notifications for expiring documents
def check_and_send_notifications():
    today = datetime.now().date()
    for employee in employee_data['Details']:
        for document_type, expiry_date in employee.items():
            if document_type.endswith('Expiry') and isinstance(expiry_date, str):
                expiry_date = datetime.strptime(expiry_date, '%d-%m-%Y').date()
                days_until_expiry = (expiry_date - today).days
                if 0 < days_until_expiry <= 10:
                    send_email_notification('kuttydevilz@gmail.com', employee['Employee Name'], document_type, str(expiry_date))

# Create a list to store the email addresses of subscribed users.
subscribers = []

# Start the app.
if __name__ == '__main__':
    # Schedule the function to check and send notifications every day
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_send_notifications, 'interval', days=1)
    scheduler.start()

    app.run(debug=True)
