import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from core.config import settings

# Введите свой логин и пароль от аккаунта.
gmail_user = settings.mail.user# 'yourlogin@gmail.com'
gmail_password = settings.mail.key  # 'your-secret-pass'

# Для подключения к серверу Google требуется использовать защищённое соединение
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(gmail_user, gmail_password)

message = EmailMessage()
message["From"] = gmail_user  # Вне зависимости от того, что вы укажете в этом поле, Gmail подставит ваши данные
message["To"] = ",".join([gmail_user])  # Попробуйте отправить письмо самому себе
message["Subject"] = 'Привет!'


env = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))  # Указываем расположение шаблонов
template = env.get_template('mail.html')  # Загружаем нужный шаблон в переменную
# В метод render передаются данные, которые нужно подставить в шаблон
output = template.render(**{
    'title': 'Новое письмо!',
    'text': 'Произошло что-то интересное! :)',
    'image': 'https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png'
})  # Заполняем шаблон нужной информацией
# В jinja2 также есть асинхронный рендер: template.render_async

# Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
# Иначе пользователю придёт набор тегов вместо красивого письма
message.add_alternative(output, subtype='html')
server.sendmail(gmail_user, [gmail_user], message.as_string())
server.close()