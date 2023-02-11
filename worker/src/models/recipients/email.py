import smtplib
from email.message import EmailMessage


class Email:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None
        self.message = EmailMessage()

    async def connect(self):
        self.connection = smtplib.SMTP(self.host, self.port)

    async def close_connect(self):
        if self.connection:
            self.connection.close()

    async def create_message(self,
                             users_to: list,
                             subject: str,
                             content: str,
                             user_from: str = "from@yandex.com",
                             ):
        self.message["From"] = user_from
        self.message["To"] = ",".join(users_to)
        self.message["Subject"] = subject
        self.message.set_content(content)

    async def send_message(self):
        return self.connection.sendmail(self.message["From"], self.message["To"], self.message.as_string())