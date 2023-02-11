import smtplib
from email.message import EmailMessage

server = smtplib.SMTP('localhost', 25)
msg['Subject'] = "Link"
msg["From"] = 'from@example.com'
msg["To"] = ",".join(['to@email.com'])

message = EmailMessage()
html = """
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

msg["Subject"] = 'Добро пожаловать в Practix!'
part1 = MIMEText('В этой фразе 25 символов.', 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
# message.set_content('В этой фразе 25 символов.')

result = server.sendmail(message["From"], ['to@email.com'], message.as_string())
server.close()