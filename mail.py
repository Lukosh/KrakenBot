import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


msg = MIMEMultipart()
msg['Subject'] = 'My Email Subject'
msg['From'] = "sender@example.com"
msg['To'] = "lucbesset.95@gmail.com"

# Create the body of the message (a plain-text and an HTML version).
text = "Hello, this is my message."
html = """\
<html>
  <head></head>
  <body>
    <p>Hello,<br>
       this is my message.
    </p>
  </body>
</html>
"""
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
msg.attach(part1)
msg.attach(part2)

# Send the email
smtp_server = 'smtp.gmail.com'
smtp_port = 465
smtp_user = 'lucbesset.95@gmail.com'
smtp_password = 'mzegkmoflrhfhzvn'
with smtplib.SMTP_SSL(smtp_server, smtp_port) as s:
    s.login(smtp_user, smtp_password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
