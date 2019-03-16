import pymysql.cursors
from flask import Flask, request
from flask_restful import Api, Resource
import datetime
import requests
import json

# Connect to the database
connection = pymysql.connect(host='sql12.freemysqlhosting.net',
                             user='sql12283501',
                             password='lkBvilxqLG',
                             db='sql12283501',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def selectDB():
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT id FROM images"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def inserDB(value, bbox):
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO images (value, timedetail,meta1) VALUES (%s, %s,%s)"
        cursor.execute(sql, (value, datetime.datetime.now(), bbox+""))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


url = 'https://bk15api.herokuapp.com/api'
IMAGEKEY = 'image'
BBOXKEY = "bbox"


class ControllerApi(Resource):

    def get(self):
        response = requests.get(url)
        json_data = json.loads(response.text)
        inserDB(json_data[IMAGEKEY], json_data[BBOXKEY])
        return {IMAGEKEY: json_data[IMAGEKEY], BBOXKEY: json_data[BBOXKEY]}

    def post(self):
        imstring = json.loads(request.data.decode('utf8').replace("'", '"'))[IMAGEKEY]
        response = requests.post(url, json={"image": imstring})
        json_data = json.loads(response.text)
        inserDB(json_data[IMAGEKEY], json_data[BBOXKEY])
        return {IMAGEKEY: json_data[IMAGEKEY], BBOXKEY: json_data[BBOXKEY]}

    def put(self):
        return {"response": "hello put"}

    def delete(self):
        return {"response": "hello delete"}


app = Flask(__name__)
api = Api(app)
api.add_resource(ControllerApi, '/api')

if __name__ == '__main__':
    app.run(debug=True)
