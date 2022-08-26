import psycopg2
from decouple import config

connect = psycopg2.connect(dbname='mew_db', user='Biomansky', password=config('DB_PASS'), port='5432',
                                  host='localhost')
cur = connect.cursor()

def create_db(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS parse ("
                "id serial PRIMARY KEY,"
                "name varchar(512),"
                "data date,"
                "value varchar(32));"
                )
    connect.commit()
    cur.close()
    connect.close()

def insert_db(cur):
    cur.execute(f'INSERT INTO parse(name, data, value) VALUES({mew}, current_date, {mew}')
create_db(cur)
