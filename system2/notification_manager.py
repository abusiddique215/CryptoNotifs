import logging
import smtplib
from email.mime.text import MIMEText

class NotificationManager:
    def __init__(self, email_config):
        self.email_config = email_config
        self.logger = logging.getLogger(__name__)
        self.notifications = {}

    def add_notification(self, coin_id, email):
        if coin_id not in self.notifications:
            self.notifications[coin_id] = set()
        self.notifications[coin_id].add(email)
        self.logger.info(f"Added notification for {coin_id} to {email}")

    def remove_notification(self, coin_id, email):
        if coin_id in self.notifications and email in self.notifications[coin_id]:
            self.notifications[coin_id].remove(email)
            self.logger.info(f"Removed notification for {coin_id} from {email}")

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

    def notify(self, coin_id, price, threshold):
        if coin_id in self.notifications:
            subject = f"Price Alert: {coin_id}"
            body = f"The price of {coin_id} has dropped below your threshold of ${threshold:.2f}. Current price: ${price:.2f}"
            for email in self.notifications[coin_id]:
                self.send_email(subject, body, email)