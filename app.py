from flask import Flask, jsonify
from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import gc
import os
import requests
from urllib.parse import urlparse
import json
from PIL import Image

from validator.image_validator import allowed_image
from image_process.process_image import open_read_image

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def root():
    return "<a href='https://github.com/aravind-tronix/Nudity-detection/blob/main/API.md''>API usage</a>"


@app.route('/url', methods=['GET', 'POST', 'OPTIONS'])
def byurl():
    if request.method == 'POST':
        data = request.get_data()
        new_str = data.decode('utf-8')
        if new_str == "":
            return json.dumps({"message": "request body is empty"})
        extracted = json.loads(new_str)
        url = extracted["url"]
        parts = url.split(".")[-1]
        if (parts == 'jpg' or 'gif' or 'png' or 'tif' or 'svg' or 'jpeg'):
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
        else:
            return jsonify({"filename": "invalid file", "ScanResult": False})
        try:
            img_data = requests.get(url).content
        except:
            return jsonify({"filename": "invalid file", "ScanResult": False})
        with open(filename, 'wb') as f:
            f.write(img_data)
        try:
            imgveri = Image.open(filename)
        except Exception as e:
            print(e)
            os.remove(filename)
            return jsonify({"filename": "invalid file", "ScanResult": False})
        Result = open_read_image(filename)
        gc.collect()
        return json.dumps({"filename": Result["filename"], "ScanResult": Result["ScannedImage"]})
    return "OK"


@app.route('/uploader',  methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            image = request.files["file"]
            if image.filename == "":
                return json.dumps({"filename": "invalid file", "ScanResult": False})
            if allowed_image(app, image.filename):
                image.save(image.filename)
                Result = open_read_image(image.filename)
                return json.dumps({"filename": Result["filename"], "ScanResult": Result["ScannedImage"]})
            else:
                return json.dumps({"filename": "invalid file", "ScanResult": False})
        return json.dumps({"filename": "invalid file", "ScanResult": False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
