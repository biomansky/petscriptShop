import psycopg2
from psycopg2 import errors
from datetime import date
from decouple import config


def db_connect():
    connect = psycopg2.connect(dbname='mew_db', user='Biomansky', password=config('DB_PASS'), port='5432',
                               host='localhost')
    return connect


def create_db():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS parse ("
                "id serial PRIMARY KEY,"
                "name varchar(512),"
                "shop varchar(32),"
                "date date,"
                "value varchar(32));"
                )
    conn.commit()
    cur.close()
    conn.close()


def insert_db(item_name, shop_name, item_price):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO parse(name, shop, date, value)'
                'VALUES(%s, %s, %s, %s)',
                (item_name, shop_name, date.today().isoformat(), item_price))
    conn.commit()
    cur.close()
    conn.close()


def select_db(limit=1):
    conn = db_connect()
    cur = conn.cursor()
    if limit == 1:
        try:
            cur.execute('SELECT date, shop, name, value '
                        'FROM parse '
                        'ORDER BY id DESC LIMIT 4')
            res = cur.fetchall()
            cur.close()
            conn.close()
            return res
        except errors.UndefinedTable:
            create_db()
    else:
        try:
            top_limit = limit * 4
            cur.execute('SELECT date, shop, name, value '
                        'FROM parse '
                        'ORDER BY id DESC LIMIT(%s)', top_limit)
            res = cur.fetchall()
            cur.close()
            conn.close()
            return res
        except errors.UndefinedTable:
            create_db()


# Функция price_diff_db() возвращает список с вложенными списками формата [['name',(shop),(value),(date)],[...],[...]]
def price_diff_db():
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute('SELECT DISTINCT name '
                    'FROM parse')
        diff_names = cur.fetchall()
        res = []
        for name in diff_names:
            name = list(name)
            cur.execute('SELECT DISTINCT shop, value, date '
                        'FROM parse '
                        'WHERE name = (%s) '
                        'ORDER BY date LIMIT 16', name)
            name_data = cur.fetchall()
            if len(name_data) != 1:
                shop_name = ''
                sdp_list = []
                for x in name_data:
                    sdp_list.extend(x[1:])
                    shop_name = x[0]
                sdp_list.insert(0, shop_name)
                name.append(tuple(sdp_list))
                res.append(name)
            else:
                name.extend(name_data)
                res.append(name)
        cur.close()
        conn.close()
        return res
    except errors.UndefinedTable:
        create_db()


x = price_diff_db()
