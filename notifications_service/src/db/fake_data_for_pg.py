import psycopg2
import random
import string
from core.config import settings

def random_string(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def random_number(n=10):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return str(random.randint(range_start, range_end))


conn = psycopg2.connect(
    host="localhost",
    database=,
    user="postgres",
    password="password"
)

cur = conn.cursor()

# create table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    );
''')

# insert fake data
fake_data = [
    (random_string() + "@email.com", random_string(), random_number())
    for i in range(10)
]

cur.executemany('''
    INSERT INTO user (email, name, phone)
    VALUES (%s, %s, %s);
''', fake_data)

conn.commit()

# close the cursor and connection
cur.close()
conn.close()
