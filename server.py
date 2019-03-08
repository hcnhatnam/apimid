import pymysql.cursors
from flask import Flask
from flask_restful import Api, Resource
import datetime

# Connect to the database
connection = pymysql.connect(host='sql12.freemysqlhosting.net',
                             user='sql12281966',
                             password='YmJr8BVWv7',
                             db='sql12281966',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def selectDB():
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT id FROM images"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def inserDB(value):
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO images (value, timedetail) VALUES (%s, %s)"
        cursor.execute(sql, (value, datetime.datetime.now()))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()



class ControllerApi(Resource):

    def get(self):
        return {"response": selectDB()}

    def post(self):
        return {"response": "hello post"}

    def put(self):
        inserDB("hello put")
        return {"response": "hello put"}

    def delete(self):
        return {"response": "hello delete"}


app = Flask(__name__)
api = Api(app)
api.add_resource(ControllerApi, '/api')

if __name__ == '__main__':
    app.run(debug=True)
