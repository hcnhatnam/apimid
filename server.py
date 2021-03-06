import pymysql.cursors
from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
from PIL import Image
import requests
import json
import uuid
import datetime
from io import BytesIO
import base64
import os

def json_serial(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def connection():
    # Connect to the database
    connection = pymysql.connect(host='remotemysql.com',
                                 user='e5mDe0T6Sv',
                                 password='2f7FLOShl7',
                                 db='e5mDe0T6Sv',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    c = connection.cursor()
    return c, connection


def selectDB():

    cursor, conn = connection()
    # Read a single record
    sql = "SELECT id FROM images"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def UpadteMeta2DB(idimage,token,meta2):

    cursor, conn = connection()
    numRow = 0
    # Create a new record
    sql = "UPDATE images SET meta2=%s WHERE id=%s AND token=%s"
    numRow = cursor.execute(sql, (meta2, idimage, token))
    conn.commit()
    return numRow




def deleteImgsDB(idsimg,token):

    cursor, conn = connection()
    numRow = 0
    format_strings = ','.join(['%s'] * len(idsimg))
    numRow = cursor.execute("DELETE FROM images WHERE id IN (%s)" % format_strings,
                            tuple(idsimg))
    # sql = "DELETE FROM images WHERE id IN (%s)"
    # numRow=cursor.execute(sql,'["2","3"]')
    # print(cursor.arraysize)
    conn.commit()
    return numRow








def inserDB(id,value, bbox,token):

    cursor, conn = connection()
    # Create a new record
    sql = "INSERT INTO images (id,value, timedetail,meta1,token) VALUES (%s,%s, %s,%s,%s)"
    cursor.execute(sql, (id, value, datetime.datetime.now(), bbox + "", token))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    conn.commit()
    return id






def selectDBbyToken(token):

    cursor, conn = connection()
    # Read a single record
    sql = "SELECT * FROM images WHERE token=%s"
    cursor.execute(sql, (token))
    result = cursor.fetchall()
    return result





def selectDBbyId(id):

    cursor, conn = connection()
    # Read a single record
    sql = "SELECT * FROM images WHERE id=%s"
    cursor.execute(sql, (id))
    result = cursor.fetchall()
    return result






urlschool = 'https://221.133.13.124:10001/p4/nam/api/'
urlheroku=" https://bk15app.herokuapp.com/p4/nam/api/"
# urlheroku="http://127.0.0.1:5010/p4/nam/api/"

HOST="0.0.0.0"
PORT="5000"

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

STATICIMAGEPATH=os.path.join("static","images")
def chooseServer(requestStr):
    if requestStr!=None:
        if requestStr=="school":
            print("===================school")
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
        #imstring = json.loads(request.data.decode('utf8').replace("'", '"'))[IMAGEKEY]
        imstring=decode.get(IMAGEKEY)
        id=str(uuid.uuid4()).replace("-","")

        im=Image.open(BytesIO(base64.b64decode(imstring)))
        pathImage=os.path.join(STATICIMAGEPATH,id+".png")
        im.save(pathImage)
        urlImage=request.url_root+pathImage

        print("urlImage",urlImage)
	#"https://iamabhik.files.wordpress.com/2011/04/32_thumb1.jpg?w=361&h=205"
        response = requests.post(url, json={"urlimage": urlImage}, verify=False)

        json_data = json.loads(response.text)
        print("id",id,"urlImage",urlImage,"json_data[BBOXKEY]",json_data[BBOXKEY])
        id=inserDB(id,urlImage, json_data[BBOXKEY],token)
        return {IDSKEY:id,IMAGEKEY: urlImage, BBOXKEY: json_data[BBOXKEY]}

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
            print("numRow",numRow)
        return {"response": numRow}


app = Flask(__name__,static_url_path='/static')
api = Api(app)
api.add_resource(ControllerApi, '/p4/nam2/api/')


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)
if __name__ == '__main__':
    if os.environ.get('APP_LOCATION') == 'heroku':
        HOST = "0.0.0.0"
        PORT = "5000"
        app.run(host=HOST, port=int(os.environ.get("PORT", PORT)))
    else:
        HOST = '127.0.0.1'
        PORT = 6010
        app.run(host=HOST, port=PORT, debug=True)


