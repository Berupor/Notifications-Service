import random

from clickhouse_driver import Client
from faker import Faker


fake = Faker()

client = Client(host='localhost')

statuses = ["ok", "error"]

#print(client.execute('SHOW TABLES FROM default;'))
#print(client.execute('SELECT * FROM default.notifications;'))

test_data = {
   "status": random.choice(statuses),
   "message": fake.text()
}

test_list = [*test_data.values()]

def create_notification():
    client.execute('''INSERT INTO default.notification (status, message) VALUES (%(status)s, %(message)s)''', test_data)

create_notification()

print(client.execute('SELECT * FROM default.notification;'))
