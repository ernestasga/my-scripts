#!/usr/bin/env python3
from email.message import EmailMessage
import os
import mimetypes
import smtplib

def generate_email(sender, receiver, subject, body, attachment):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(body)
    
    filename = os.path.basename(attachment)
    mime_type, _ = mimetypes.guess_type(attachment)
    mime_type, mime_subtype = mime_type.split('/', 1)

    with open(attachment, 'rb') as pdf:
        message.add_attachment(pdf.read(), maintype=mime_type, subtype=mime_subtype, filename=filename)
        pdf.close()
    return message

def send_email(message):
    mail_server = smtplib.SMTP('localhost')
    mail_server.send_message(message)
    mail_server.quit()

def generate_error_report(sender, receiver, subject, body):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.set_content(body)

    return message