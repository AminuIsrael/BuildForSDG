from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(subject,email_address,messageToSend):
    msg = MIMEMultipart()
    message = messageToSend
    password = "Am1nuIsr2"
    msg['From'] = "aminuisrael90@gmail.com"
    msg['To'] = email_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.login(msg['From'], password)
    server.quit()