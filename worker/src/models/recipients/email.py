import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import BaseLoader, Environment


class Email:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None
        self.message = MIMEMultipart("alternative")

    async def connect(self):
        self.connection = smtplib.SMTP(self.host, self.port)

    async def close_connect(self):
        if self.connection:
            self.connection.close()

    async def create_message(
        self,
        users_to: list,
        data: dict,
        template: str,
        user_from: str = "from@yandex.com",
    ):
        self.message["From"] = user_from
        self.message["To"] = ",".join(users_to)
        rtemplate = Environment(loader=BaseLoader).from_string(template)
        for user in users_to:
            html = rtemplate.render({"user": user, "film": data.get("movies")})
            self.message.attach(MIMEText(html, "html"))
            yield self.message

    async def send_message(self, message: MIMEMultipart):
        return self.connection.sendmail(
            message.get("From"), message.get("To"), message.as_string()
        )
