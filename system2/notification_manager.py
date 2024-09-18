import logging
import smtplib
from email.mime.text import MIMEText

class NotificationManager:
    def __init__(self, email_config):
        self.email_config = email_config
        self.logger = logging.getLogger(__name__)

    def send_email(self, subject, body, to_email):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.email_config['from_email']
            msg['To'] = to_email

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['username'], self.email_config['password'])
                server.send_message(msg)

            self.logger.info(f"Notification sent to {to_email}")
        except Exception as e:
            self.logger.error(f"Failed to send notification: {str(e)}")

    def notify(self, coin_id, price, threshold, to_email):
        subject = f"Price Alert: {coin_id}"
        body = f"The price of {coin_id} has dropped below ${threshold}. Current price: ${price}"
        self.send_email(subject, body, to_email)