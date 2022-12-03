import sqlite3

DATABASE = 'database.db'

def create_table():
    create = "CREATE TABLE IF NOT EXISTS games (title, price, description, link)"

    connect = sqlite3.connect(DATABASE)
    connect.execute(create)

    connect.close()

def get_table():
    get = "SELECT * FROM games"

    connect = sqlite3.connect(DATABASE)

    return connect.execute(get)

def add_table(title, price, description, link):

    connect = sqlite3.connect(DATABASE)
    connect.execute('INSERT INTO games VALUES (?, ?, ?, ?)', [title, price, description, link])
    connect.commit()