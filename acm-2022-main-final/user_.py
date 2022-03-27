import sqlite3
from flask_restful import Resource, reqparse

class User(object):
    TABLE_NAME = 'users'

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        return row

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        conn.close()
        return user
    
    @classmethod
    def update_data(cls, username, data):
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        print(data, type(data))
        row = cls.find_by_username(username)
        print(username)
        print(type(row))
        query = "UPDATE users SET data = ? WHERE username = ?"
        if row[3] is not None:
            cursor.execute(query, (row[3] + "," + data,username,))
        else:
            cursor.execute(query, (data,username,))
        conn.commit()
        

class UserRegister(Resource):
    TABLE_NAME = 'users'
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_id(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES (NULL, ?, ?, NULL)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
