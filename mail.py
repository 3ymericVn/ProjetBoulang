import smtplib
from email.mime.text import MIMEText
from env import EMAIL, PASSWORD


def send_mail(subject: str, body: str, recipients: list[str]):
   msg = MIMEText(body)
   msg['Subject'] = subject
   msg['From'] = EMAIL
   msg['To'] = ', '.join(recipients)
   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
      smtp_server.login(EMAIL, PASSWORD)
      smtp_server.sendmail(EMAIL, recipients, msg.as_string())
   print("Message sent!")
