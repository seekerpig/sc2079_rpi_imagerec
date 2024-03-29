import argparse
import io
import torch
from flask import Flask, request, jsonify
from PIL import Image
import glob
from imutils import paths
import os
import time
import cv2
import numpy as np

app = Flask(__name__)

DETECTION_URL = "/Test"

# flask connection



@app.route("/")
def home():
    return "<h1>Welcome to the HomePage!</h1>"


@app.route(DETECTION_URL, methods=["POST"])
def predict():

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))
        # Resize the image to a width of 640 pixels while preserving the aspect ratio
        #img_resized = img.resize((640, int(img.size[1] * 640 / img.size[0])))
        #img.save('raw')
        # Get the current time as a string
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        # Create the raw folder if it doesn't exist
        os.makedirs('raw', exist_ok=True)

        # Use the timestamp in the file name to save the raw image in the raw folder
        img.save(f'raw/raw_{timestamp}.jpg')

        results = model(img, size=640)
        results.save('runs')
        stitch_image()
        
        df_results = results.pandas().xyxy[0]
        print(df_results)


            
            
        df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
        df_results['bboxWt'] = df_results['xmax'] - df_results['xmin']
        df_results['bboxArea'] = df_results['bboxHt'] * df_results['bboxWt']

        
        df_results = df_results.sort_values('bboxArea', ascending=True)  # Label with largest bbox height will be last
        
        if len(df_results)>1:
            if abs(df_results['ymax'][0] - df_results['ymax'][1]) <=20 or abs(df_results['ymin'][0] - df_results['ymin'][1]) <=20 or abs(df_results['xmin'][0] - df_results['xmin'][1]) <=20 or abs(df_results['xmax'][0] - df_results['xmax'][1]) <=20:
                print("Yes")
                df_results = df_results.sort_values('confidence', ascending=True)  # Label with largest bbox height will be last
            
        
        #pred4 = df_results['confidence'].to_numpy()
        #print(pred4) 
        #if pred4[-1] < 0.8:
        #    image_id = 'NA'
        #    result = {"image_id": image_id}
        #    return jsonify(result)
            
        print(df_results)
        pred_list = df_results['name'].to_numpy()
        pred = 'NA'

        if pred_list.size > 0:
            for i in pred_list:
                #if i != '41': #need to remove for bullseye testing
                    pred = i


        Symbol_Map_to_id = {
            "NA": 'NA',
            "38": 38,
            "39": 39,
        }

        image_id = Symbol_Map_to_id.get(pred, 'NA')
        result = {"image_id": image_id}
        print(result)

        return jsonify(result)


def stitch_image():
    imgFolder = 'runs'
    newPath = 'uploads/stitched.jpg'
    imgPath = list(paths.list_images(imgFolder))
    images = [Image.open(x) for x in imgPath]
    # Filter images with label "Bullseye"
    #filtered_images = [img for img in images if "41" not in img]
    #width, height = zip(*(i.size for i in images))
    width, height = zip(*(img.size for img in images))
    total_width = sum(width)
    max_height = max(height)
    stitchedImg = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        stitchedImg.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    stitchedImg.save(newPath)


def load_model():
    model = torch.hub.load('./yolov5/', 'custom', path='yolov5/arrows2', source='local')
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5005, type=int, help="port number")
    args = parser.parse_args()
    model = load_model()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
