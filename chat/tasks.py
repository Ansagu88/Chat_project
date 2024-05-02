import smtplib
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from celery import shared_task
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = settings.SMTP_SERVER
smtp_port = settings.SMTP_PORT
email = settings.EMAIL
password = settings.PASSWORD

def send_email(user):
    """
    Sends an email to the specified user.

    Parameters:
    - user: User object representing the recipient of the email.

    Returns:
    None
    """
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = user.email
    msg['Subject'] = 'Deleted ChatGptApp User'
    message = 'Dear, {} as we reported at the beginning, User {} has been removed after 24 hours of its creation, we thank you for your trust in our site. Best regards'.format(user.first_name, user.username)
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP(smtp_server, smtp_port)
    mailServer.starttls()
    mailServer.login(email, password)
    mailServer.sendmail(email, user.email, msg.as_string())
    mailServer.close()

@shared_task
def check_users():
    """
    Checks the users in the database and deletes those who have been created more than 24 hours ago.
    Sends an email to each deleted user.

    Parameters:
    None

    Returns:
    None
    """
    users = User.objects.all()
    for user in users:
        if not user.is_superuser and timezone.now() - user.date_joined > timedelta(hours=24):
            send_email(user)
            user.delete()
