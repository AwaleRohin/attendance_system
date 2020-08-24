from flask import Flask, jsonify, request
import boto3
from flask_cors import CORS
import time
import base64

app = Flask(__name__)
CORS(app)
client = boto3.client('rekognition')

@app.route('/create-colection', methods=['GET'])
def create_collection():
    response = client.create_collection(
        CollectionId='TestEmployeeCollection'
    )
    content = jsonify({
        "status":True,
        "data": "Created Collection"
    })
    return content, 201

@app.route('/add')
def add_faces():
    CollectionId='TestEmployeeCollection'
    response = client.index_faces(
        CollectionId = CollectionId,
        Image = {
            'Bytes':request.files['image']
        },
        ExternalImageId='Rohin'
    )
    print(response)

@app.route('/', methods=["POST"])
def detect_faces():
    data = request.get_json()
    filename = convert_and_save(data['image'])
    image = open(filename, 'rb').read()
    CollectionId = 'TestEmployeeCollection'
    response = client.detect_faces(
        Image={
            'Bytes': image
        }
    )
    if(len(response['FaceDetails']) > 0):
        res = client.search_faces_by_image(
            CollectionId=CollectionId,
            Image={
                'Bytes': image
            }
        )
        content = jsonify({
            "status":True,
            "data": "Face Matched. Attendance done for the day"
        })
        return content, 200
    else:
        content =  jsonify({
            "status":False,
            "data": "No Match found"
        })
        return content, 200


def convert_and_save(data):
    file = "{}.jpg".format(time.time())
    data = data.split(',')
    image_code = base64.b64decode(data[1])
    with open(file, 'wb') as f:
        f.write(image_code)
    return file