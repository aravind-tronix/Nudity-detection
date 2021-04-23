from flask import Flask, jsonify
from flask import Flask, render_template, request,redirect
from flask_cors import CORS
import gc
import os
import requests
from urllib.parse import urlparse
import json
from PIL import Image
import base64
import telegram
from datetime import date
import uuid
import numpy as np
import time
from datetime import date

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
       

def open_img(filename):
    import cv2

    labelsPath = "./CustomConfigs/obj.names"
    LABELS = open(labelsPath).read().strip().split("\n")

    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    # derive the paths to the YOLO weights and model configuration
    # give path where you have stored yolov3.weights file and rename the file as yolov3
    weightsPath = "custom_weights.weights"

    # give path where you have stored yolov3.cfg file and rename the file as yolov3
    configPath = "./CustomConfigs/custom.cfg"

    # load our YOLO object detector trained on COCO dataset
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    # load our input image and grab its spatial dimensions
    image = cv2.imread(filename)
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # show timing information on YOLO

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                    # extract the class ID and confidence (i.e., probability) of
                    # the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > 0.3:
                            # scale the bounding box coordinates back relative to the
                            # size of the image, keeping in mind that YOLO actually
                            # returns the center (x, y)-coordinates of the bounding
                            # box followed by the boxes' width and height
                            box = detection[0:4] * np.array([W, H, W, H])
                            (centerX, centerY, width, height) = box.astype("int")

                            # use the center (x, y)-coordinates to derive the top and
                            # and left corner of the bounding box
                            x = int(centerX - (width / 2))
                            y = int(centerY - (height / 2))

                            # update our list of bounding box coordinates, confidences,
                            # and class IDs
                            boxes.append([x, y, int(width), int(height)])
                            confidences.append(float(confidence))
                            classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.3,0.3 )



    # count the number of persons

    # ensure at least one detection exists
    if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                    
                    if(  LABELS[classIDs[i]])=='nude':
                            # extract the bounding box coordinates
                            (x, y) = (boxes[i][0], boxes[i][1])
                            (w, h) = (boxes[i][2], boxes[i][3])
                            
                            # draw a bounding box rectangle and label on the image
                            color = [int(c) for c in COLORS[classIDs[i]]]
                            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5, color, 2)
                            ScannedImage="Private parts exposed"
                    else:
                            ScannedImage="Private parts exposed"
    else:
            ScannedImage="Nothing exposed"
    os.remove(filename)
    image = None
    idxs = None
    net = None
    COLORS = None
    classIDs = None
    confidences = None
    boxes = None
    cv2 = None
    layerOutputs = None 
    return {"filename":filename,"ScannedImage":ScannedImage}



@app.route('/url', methods = ['GET', 'POST','OPTIONS'])
def byurl():
   if request.method == 'POST':
        data = request.get_data()
        new_str = data.decode('utf-8')
        d = json.loads(new_str)
        url = d["url"]
        parts = url.split(".")[-1]
        if (parts =='jpg'or 'gif' or 'png' or 'tif' or 'svg' or 'jpeg'):
            a = urlparse(url)
            filename = os.path.basename(a.path)
        else:
            return jsonify({"filename":"invalid file","ScanResult":False})
        try:
            img_data = requests.get(url).content
        except:
            return jsonify({"filename":"invalid file","ScanResult":False})
        with open(filename, 'wb') as f:
            f.write(img_data)
        try:
            imgveri = Image.open(filename)
        except Exception as e:
            print(e)
            os.remove(filename)
            return jsonify({"filename":"invalid file","ScanResult":False})
        Result = open_img(filename)
        gc.collect()
        return json.dumps({"filename":Result["filename"],"ScanResult":Result["ScannedImage"]})
   return "OK"

@app.route('/uploader',  methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if request.files: 
            image = request.files["file"]
            if image.filename == "":
                return json.dumps({"filename":"invalid file","ScanResult":False})
            if allowed_image(image.filename):
                image.save(image.filename)
                Result = open_img(image.filename)
                return json.dumps({"filename":Result["filename"],"ScanResult":Result["ScannedImage"]})
            else:
                print("That file extension is not allowed")
                return json.dumps({"filename":"invalid file","ScanResult":False})
        return json.dumps({"filename":"invalid file","ScanResult":False})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug= True)
