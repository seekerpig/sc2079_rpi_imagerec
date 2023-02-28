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


        results = model(img, size=640)  # reduce size=320 for faster inference
        results.save('runs')
        stitch_image()
        # return results.pandas().xyxy[0].to_json(orient="records")
        df_results = results.pandas().xyxy[0]

        df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
        df_results['bboxWt'] = df_results['xmax'] - df_results['xmin']
        df_results['bboxArea'] = df_results['bboxHt'] * df_results['bboxWt']

        df_results = df_results.sort_values('bboxArea', ascending=True)  # Label with largest bbox height will be last
        print(df_results.to_string(index=False))
        print(df_results)
        pred_list = df_results['name'].to_numpy()
        pred = 'NA'


        if pred_list.size > 0:
            for i in pred_list:
                #if i != '41': #need to remove for bullseye testing
                    pred = i

        for i in df_results:
                image_id = i[0]
                bbox = i[2]
                x_coordinate = int(bbox[0])
                height = int(bbox[3])

                # calculate distance
                if height > 190:
                    distance = 15
                elif height > 170:
                    distance = 20
                elif height > 150:
                    distance = 25
                elif height > 133:
                    distance = 30
                elif height > 117:
                    distance = 35
                elif height > 95:
                    distance = 40
                elif height > 85:
                    distance = 45
                elif height > 78:
                    distance = 50
                elif height > 72:
                    distance = 55
                elif height > 64:
                    distance = 60
                elif height > 61:
                    distance = 65
                elif height > 58:
                    distance = 70
                else:
                    distance = 75
                    # 52 is height of 80 cm

                # calculate position
                if x_coordinate < 83:
                    position = "LEFT"
                elif x_coordinate < 166:
                    position = "CENTRE"
                else:
                    position = "RIGHT"
                    # 250 is maximum

        Symbol_Map_to_id = {
            "NA": 'NA',
            "11": 11, #1
            "12": 12, 
            "13": 13,
            "14": 14,
            "15": 15,
            "16": 16,
            "17": 17,
            "18": 18,
            "19": 19,
            "20": 20,
            "21": 21,
            "22": 22,
            "23": 23,
            "24": 24,
            "25": 25,
            "26": 26,
            "27": 27,
            "28": 28,
            "29": 29,
            "30": 30,
            "31": 31,
            "32": 32,
            "33": 33,
            "34": 34,
            "35": 35,
            "36": 36,
            "37": 37,
            "38": 38,
            "39": 39,
            "40": 40,
            "41": 41
        }

        image_id = Symbol_Map_to_id.get(pred, 'NA')
        result = {"image_id": image_id}

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
    model = torch.hub.load('./yolov5/', 'custom', path='yolov5/besty.pt', source='local')
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5005, type=int, help="port number")
    args = parser.parse_args()
    model = load_model()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
