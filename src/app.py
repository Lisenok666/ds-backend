import logging
import requests
from flask import Flask, request
from PIL import Image
from models.plate_reader import PlateReader, InvalidImage
import logging
import json 
import base64
import io


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')

def function_load_images(imageID):
    try:
        response = requests.get(imageID)
    except:
        return {'error': 'Connection failed'}, 500

    if response.status_code != 200:
        return {'error': 'Uncorrect "imageID"'}, 401

    return {
        'result': (response.content).decode('ISO-8859-1'),
    }

@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {
        'plate_number': res,
    }

# <url>:8080 : body: {"imageID": "http://51.250.83.169:7878/images/10022"}
@app.route('/loadImage',methods = ['POST'])
def load_image():
    if 'imageID' not in request.json:
        return {'error': 'field "imageID" not found'}, 400

    imageID = request.json['imageID']
    return  function_load_images(imageID)


@app.route('/loadImages',methods = ['POST'])
def load_images():
    if 'imagesID' not in request.json:
        return {'error': 'field "imagesID" not found'}, 400

    imagesID = request.json['imagesID']
    ret = {}
    for imageID in imagesID:
        ret[imageID] = function_load_images(imageID)
    return ret
    


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
