import pymysql.cursors
from flask import Flask, request
from flask_restful import Api, Resource

import requests
import json

import datetime

def json_serial(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
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

def UpadteMeta2DB(idimage,token,meta2):
    numRow=0
    with connection.cursor() as cursor:
        # Create a new record
        sql = "UPDATE images SET meta2=%s WHERE id=%s AND token=%s"
        numRow=cursor.execute(sql, (meta2, idimage, token))
    connection.commit()
    return numRow

def inserDB(value, bbox,token):
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO images (value, timedetail,meta1,token) VALUES (%s, %s,%s,%s)"
        cursor.execute(sql, (value, datetime.datetime.now(), bbox+"",token))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
def selectDBbyToken(token):
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM images WHERE token=%s"
        cursor.execute(sql,(token))
        result = cursor.fetchall()
        return result

def selectDBbyId(id):
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM images WHERE id=%s"
        cursor.execute(sql,(id))
        result = cursor.fetchall()
        return result

url = 'https://bk15api.herokuapp.com/api'
IMAGEKEY = 'image'
TOKENKEY = 'token'
BBOXKEY = "bbox"
GETTYPEKEY="gettype"
DATAGETKEY="data"
PUTTYPEKEY="puttype"
IDIMAGEKEY = 'idimage'
IDSKEY="ids"
META2KEY="meta2"
class ControllerApi(Resource):

    def get(self):
        result=""
        gettype = request.args.get(GETTYPEKEY)
        if gettype=="history":
            token = request.args.get(DATAGETKEY)
            result= selectDBbyToken(token)
        elif gettype=="idget":
            id = request.args.get(DATAGETKEY)
            result = selectDBbyId(id)
        return json.loads(json.dumps(result,default=json_serial))


    def post(self):
        token = json.loads(request.data.decode('utf8'))[TOKENKEY]
        imstring = json.loads(request.data.decode('utf8').replace("'", '"'))[IMAGEKEY]
        response = requests.post(url, json={"image": imstring})
        json_data = json.loads(response.text)
        inserDB(json_data[IMAGEKEY], json_data[BBOXKEY],token)
        return {IMAGEKEY: json_data[IMAGEKEY], BBOXKEY: json_data[BBOXKEY]}

    def put(self):
        numRow=0
        # try:
        puttype = json.loads(request.data.decode('utf8'))[PUTTYPEKEY]
        print("puttype", puttype)

        if puttype=="content":
            token = json.loads(request.data.decode('utf8'))[TOKENKEY]
            idimage = json.loads(request.data.decode('utf8'))[IDIMAGEKEY]
            meta2 = json.loads(request.data.decode('utf8'))[META2KEY]
            print("put",token,idimage,meta2)
            numRow=UpadteMeta2DB(idimage, token, meta2)
        return {"response": numRow}
        # except:
        #     return {"response": numRow}

    def delete(self):
        return {"response": "deleted"}


app = Flask(__name__)
api = Api(app)
api.add_resource(ControllerApi, '/api')

if __name__ == '__main__':
    app.run(debug=True)
