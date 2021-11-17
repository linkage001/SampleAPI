from flask import Flask, redirect, url_for, request
import threading
import json

from database import Database


class FlaskThread:
    db = Database()

    def __init__(self):
        app = Flask(__name__)

        @app.route("/", methods=['POST', 'GET'])
        def unspecified():
            return 'HTTP 404 Not Found', 404

        @app.route("/users/", methods=['POST', 'GET', 'DELETE'])
        def users():
            user = ''

            # Delete
            if request.method == 'DELETE':
                user_token = request.form['token']
                if self.db.delete(token=user_token):
                    return 'Delete success'
                else:
                    return 'Delete fail'

            # Register
            if request.method == 'GET' or request.method == 'POST':
                if request.method == 'POST':
                    user = request.form.get('username', '')
                if request.method == 'GET':
                    user = request.args.get('username', '')
                if user == '':
                    return 'Invalid user, 403', 403
                if not self.db.login(user):
                    self.db.register(user)
                    token = self.db.get_user_data(user)['token']
                    response = {'token': token}
                    return json.dumps(response), 200
                else:
                    return 'User Already Exists', 403

        # TODO: Delete shopping list by name
        # TODO: Make shopping list
        @app.route("/shop_list/", methods=['POST', 'GET', 'DELETE'])
        def shop_list():
            # Sample list
            # items = ['poulet',
            #          'bœuf',
            #          'porc',
            #          'patate',
            #          'carotte',
            #          'brocoli',
            #          'oignon',
            #          'cumin',
            #          'piment']
            return 'TODO'

        arg = ('0.0.0.0', 80,)
        threading.Thread(target=app.run, args=arg).start()