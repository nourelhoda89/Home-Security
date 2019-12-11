import smtplib, ssl
from datetime import datetime

def send():
    # datetime object containing current date and time
    now = datetime.now()
     


    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "sender email"
    receiver_email = "receiver email"
    password = "your password"
    message = """\
    Subject: Intruder Alert

    Our Secutity sensor detected an Intruder. \nDate and time ="""+ dt_string

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
