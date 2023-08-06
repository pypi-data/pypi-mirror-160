#!/usr/bin/python3
# -*- coding: utf-8 -*-
import configparser
import smtplib
from email.mime.base import MIMEBase
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_base64
from getpass import getpass
import time
import os
from os.path import basename
import sys
import csv

TRUE_STRINGS = ('true', 'True', 'yes', 'Yes')

def send_emails(config_file, body_file, student_file='students.csv', dryrun=False):
    config = configparser.ConfigParser()
    config.read(config_file)
    from_address = config['DEFAULT']['FROM_ADDRESS']
    with open( body_file, 'r') as f:
        body_template = f.read()

    ###########################

    if not dryrun:
        smtppass = getpass('email password, please:')
        server = smtplib.SMTP_SSL(config['DEFAULT']['SMTPSERVER'], config['DEFAULT']['SMTPPORT'])
        print( server.ehlo())

        if config['DEFAULT']['AUTHREQUIRED']:
            print (server.login(config['DEFAULT']['SMTPUSER'], smtppass))

    ###########################
    data = list(csv.reader(open(student_file, 'r')))
    fields = data[0]
    student_data = data[1:]
    indices = {field:i for i,field in enumerate(fields)}
    attachment_string = config['DEFAULT'].get('ATTACHMENT')
    html_string = config['DEFAULT'].get('HTML')

    for row in student_data:
        if not row: continue
        email = row[indices['email']]
        student_dict = {field:row[indices[field]] for field in fields}
        attachments = []
        if attachment_string:
            if attachment_string in TRUE_STRINGS:
                attachment_paths = row[indices['attachment']]
            else:
                attachment_paths = attachment_string.format(**student_dict)
            try:
                for attachment_path in attachment_paths.split(','):
                    attachment_name = basename(attachment_path)
                    attachment_ext  = os.path.splitext(attachment_name)[-1]
                    with open(attachment_path, 'rb') as file:
                        attachment = MIMEApplication(
                            file.read(),
                            _subtype=attachment_ext,
                            Name=attachment_name
                        )
                    attachment.add_header('Content-Disposition', 'attachment; filename="%s"'%attachment_name)
                    attachments.append((attachment_path, attachment_name, attachment))
            except FileNotFoundError:
                print('Missing file:', attachment_path)
                print('   No email sent to', email)
                continue

        toaddrs = [email, from_address]
        body = body_template.format(**student_dict)

        msg = MIMEMultipart()
        msg['Subject'] = config['DEFAULT']['SUBJECT']
        msg['To'] = email
        msg['From'] = from_address
        part2 = MIMEText(
            body,
            'html' if html_string in TRUE_STRINGS else 'plain',
            'utf8')
        msg.attach(part2)
        if attachments:
            for attachment_path, attachment_name, attachment in attachments:
                msg.attach(attachment)
        #Send
        try:
            if email.split('@')[1]=='example.com' or dryrun:
                print('example email to', email)
                print(body)
            else:
                smtpresult = server.sendmail(from_address, [email, from_address], msg.as_string())
            print ('ok', email)
        except Exception as e:
            print ('There was an error sending the message to: %s'%email)
            print(e)

        time.sleep(int(config['DEFAULT']['DELAY']))

    if not dryrun:
        server.close()
