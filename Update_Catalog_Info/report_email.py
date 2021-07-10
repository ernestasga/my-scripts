#!/usr/bin/env python3
import os
from datetime import date
from reports import generate_report
import emails

def process_data():
    text_files_dir = './supplier-data/descriptions'
    descr_files = [file for file in os.listdir(text_files_dir)]   
    summary = ''
    for file in descr_files:
        path = os.path.join(text_files_dir, file)
        with open(path) as txt:
            for i, line in enumerate(txt.readlines()):
                if i == 0:
                    summary += "name: {}<br/>".format(line.strip())
                elif i == 1:
                    summary += "weight: {}<br/><br/>".format(line.strip())
            txt.close()
    return summary

if __name__ == "__main__":
    attachment = 'processed.pdf'
    # Generate report
    title = "Processed Update on {}".format(date.today())
    summary = process_data()
    generate_report(attachment, title, summary)

    # Send email
    sender = 'automation@example.com'
    receiver = '{}@example.com'.format(os.environ.get('USER'))
    subject = 'Upload Comleted - Online Fruit Store'
    body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.'

    message = emails.generate_email(sender, receiver, subject, body, attachment)
    emails.send_email(message)



