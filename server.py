import pymysql.cursors
from flask import Flask, request
from flask_restful import Api, Resource

import requests
import json
import uuid
import datetime
def json_serial(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
# Connect to the database
connection = pymysql.connect(host='remotemysql.com',
                             user='e5mDe0T6Sv',
                             password='2f7FLOShl7',
                             db='e5mDe0T6Sv',
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
def deleteImgsDB(idsimg,token):
    numRow=0
    with connection.cursor() as cursor:
        format_strings = ','.join(['%s'] * len(idsimg))
        numRow=cursor.execute("DELETE FROM images WHERE id IN (%s)" % format_strings,
                       tuple(idsimg))
        # sql = "DELETE FROM images WHERE id IN (%s)"
        # numRow=cursor.execute(sql,'["2","3"]')
        # print(cursor.arraysize)
    connection.commit()
    return numRow

def inserDB(value, bbox,token):

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO images (id,value, timedetail,meta1,token) VALUES (%s,%s, %s,%s,%s)"
        id=str(uuid.uuid4())
        cursor.execute(sql, (id,value, datetime.datetime.now(), bbox+"",token))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    return id
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

urlschool = 'https://bk15api.herokuapp.com/api'
urlheroku=" https://bk15app.herokuapp.com/p4/nam/api/"
IMAGEKEY = 'image'
TOKENKEY = 'token'
BBOXKEY = "bbox"
GETTYPEKEY="gettype"
DATAGETKEY="data"
PUTTYPEKEY="puttype"
DELETETYPEKEY="deletetype"
IDIMAGEKEY = 'idimage'
IDSKEY="ids"
META2KEY="meta2"
SERVERTYPE="servertype"
def chooseServer(requestStr):
    if requestStr!=None:
        if requestStr=="school":
            return urlschool
    return urlheroku
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
        decode=json.loads(request.data.decode('utf8'))

        url=chooseServer(decode.get(SERVERTYPE))
        token = decode.get(TOKENKEY)
        # imstring = json.loads(request.data.decode('utf8').replace("'", '"'))[IMAGEKEY]
        imstring=decode.get(IMAGEKEY)
        response = requests.post(url, json={"image": imstring})
        json_data = json.loads(response.text)
        id=inserDB(json_data[IMAGEKEY], json_data[BBOXKEY],token)
        return {IDSKEY:id,IMAGEKEY: json_data[IMAGEKEY], BBOXKEY: json_data[BBOXKEY]}

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
        numRow = 0
        deletetype = json.loads(request.data.decode('utf8'))[DELETETYPEKEY]
        print("deletetype", deletetype)
        if deletetype == "deleteimg":
            token = json.loads(request.data.decode('utf8'))[TOKENKEY]
            idimage = json.loads(request.data.decode('utf8'))[IDIMAGEKEY]
            print("delete", token, idimage)
            numRow = deleteImgsDB(idimage, token)
        return {"response": numRow}


app = Flask(__name__)
api = Api(app)
api.add_resource(ControllerApi, '/p4/nam2/api/')
import os
if __name__ == '__main__':
    if os.environ.get('APP_LOCATION') == 'heroku':
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        app.run(host='127.0.0.1', port=6010, debug=True)


