import smtplib
from email.message import EmailMessage


def mailSender(subject, message, sender, receiver, password):
    msg = EmailMessage()
    msg.set_content(message)
    msg['subject'] = subject
    msg['to'] = receiver
    msg['from'] = sender
    
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.send_message(msg)
    
    server.quit()