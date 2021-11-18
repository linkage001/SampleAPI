from flask_thread import FlaskThread
import sqlite3

if __name__ == '__main__':

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE IF NOT EXISTS 'users' ( 
              'id' INTEGER PRIMARY KEY AUTOINCREMENT, 
              'username'  TEXT,     
              'token'  TEXT );
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS 'shoppingLists' ( 
              'id' INTEGER PRIMARY KEY AUTOINCREMENT, 
              'userID'  INTEGER);
              ''')

    conn.commit()

    ft = FlaskThread()



