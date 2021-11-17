import sqlite3 as sql
import secrets

# TODO: Protect from SQL injection
class Database:
    db = 'C:\\Users\\William\\data.db'

    def get_user_data(self, username, token=''):
        con = sql.connect(self.db)
        cur = con.cursor()
        data_dict = {}

        if token != '':
            statement = f"SELECT * from users WHERE token='{token}';"
        else:
            statement = f"SELECT * from users WHERE username='{username}';"
        cur.execute(statement)
        data_list = cur.fetchone()
        if not data_list:
            print('get_user_data failed: ' + username + ' ' + token)
            return data_dict

        data_dict['id'] = data_list[0]
        data_dict['username'] = data_list[1]
        data_dict['token'] = data_list[2]
        print(data_dict)
        con.close()
        return data_dict

    def create_shopping_list(self, username, items):

        user_data = self.get_user_data(username)
        con = sql.connect(self.db)
        cur = con.cursor()
        statement = f"INSERT INTO 'shoppingLists' ('userID') VALUES ('{user_data['id']}');"
        cur.execute(statement)
        con.commit()
        listID = cur.lastrowid
        statement = f"CREATE TABLE IF NOT EXISTS shopping_list_{listID} ('id' INTEGER PRIMARY KEY AUTOINCREMENT , 'item'  INTEGER);"
        cur.execute(statement)
        con.commit()

        for item in items:
            statement = f"INSERT INTO shopping_list_{listID} ('item') VALUES ('{item}');"
            cur.execute(statement)
            con.commit()

        con.close()

    def login(self, username):
        con = sql.connect(self.db)
        cur = con.cursor()
        statement = f"SELECT id from users WHERE username='{username}';"
        cur.execute(statement)
        result = cur.fetchone()
        con.close()
        if not result:
            print('Login failed')
            return False
        else:
            print('Login success: ' + str(result[0]))
            return True

    def register(self, username):
        if not self.login(username):
            token = secrets.token_urlsafe()
            con = sql.connect(self.db)
            cur = con.cursor()
            statement = f"INSERT INTO 'users' ('username', 'token') VALUES ('{username}', '{token}');"
            cur.execute(statement)
            result = cur.fetchone()
            con.commit()
            if result:
                print(str(result[0]))
            statement = f"SELECT id from users WHERE username='{username}';"
            cur.execute(statement)
            result = cur.fetchone()
            if result:
                print('Register success: ' + str(result[0]))
            con.close()

        else:
            print('Register failed: user already exists')


    # TODO: rename to delete_user & make delete_list OR make this general purpuse
    def delete(self, username='', token=''):

        user_data = self.get_user_data(username, token)

        # Fail on no data found from token, username
        if not bool(user_data.get('username')):
            return False

        # Fail on invalid token for username
        if token != user_data['token']:
            print('Delete failed: Invalid token')
            return False


        con = sql.connect(self.db)
        cur = con.cursor()
        statement = f"DELETE FROM 'users' WHERE username='{user_data.get('username')}';"
        cur.execute(statement)
        result = cur.fetchone()
        con.commit()
        if not result:
            statement = f"SELECT token from users WHERE username='{user_data.get('username')}';"
            cur.execute(statement)
            result = cur.fetchone()
            if not result:
                print('Delete success')
                return True
        else:
            print(result[0])
            return False
        con.close()
