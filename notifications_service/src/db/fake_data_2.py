import psycopg2
import random
import string
from core.config import settings


def random_string(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generate_random_html(n=10):
    html = "<html>"
    for i in range(n):
        html += "<p>" + random_string() + "</p>"
    html += "</html>"
    return html


conn = psycopg2.connect(
    host="localhost",
    database=settings.postgres.dbname,
    user=settings.postgres.user,
    password=settings.postgres.password
)

cur = conn.cursor()

# create table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS template (
        id SERIAL PRIMARY KEY,
        html TEXT NOT NULL,
        event_name VARCHAR(255) NOT NULL UNIQUE
    );
''')

# insert fake data
fake_data = [
    (generate_random_html(), 'user_register')
    for i in range(1)
]

cur.executemany('''
    INSERT INTO "template" (html, event_name)
    VALUES (%s, %s);''', fake_data)

conn.commit()

# close the cursor and connection
cur.close()
conn.close()
