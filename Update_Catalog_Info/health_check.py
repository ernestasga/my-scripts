#!/usr/bin/env python3
import os
import psutil
import shutil
import socket
import emails

def check_cpu_usage(max):
    return psutil.cpu_percent(1) < max

def check_disk_usage(disk, min_percent):
    disk = shutil.disk_usage(disk)
    disk_available = (disk.free/disk.total*100)
    return disk_available > min_percent

def check_available_memory(min_mb):
    available_memory = psutil.virtual_memory().available / (1024**2)
    return available_memory > min_mb

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'

checks = {
    check_cpu_usage(80): 'Error - CPU usage is over 80%',
    check_disk_usage('/', 20): 'Error - Available disk space is less than 20%',
    check_available_memory(500): 'Error - Available memory is less than 500MB',
    check_localhost(): 'Error - localhost cannot be resolved to 127.0.0.1'
}
sender = 'automation@example.com'
receiver = '{}@example.com'.format(os.environ.get('USER'))
email_body = 'Please check your system and resolve the issue as soon as possible.'

for check, error in checks.items():
    if not check:
        try:
            message = emails.generate_error_report(sender, receiver, error, email_body)
            emails.send_email(message)
        except:
            print("Error while sending email")
