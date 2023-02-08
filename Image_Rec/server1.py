import argparse
import io
import torch
from flask import Flask, request, jsonify
from PIL import Image
import glob
from imutils import paths
import os
import time

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
        print(df_results)
        pred_list = df_results['name'].to_numpy()
        pred = 'NA'

        if pred_list.size > 0:
            for i in pred_list:
                if i != 'Bullseye':
                    pred = i

        Symbol_Map_to_id = {
            "NA": 'NA',
            "11": 11,
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
    width, height = zip(*(i.size for i in images))
    total_width = sum(width)
    max_height = max(height)
    stitchedImg = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        stitchedImg.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    stitchedImg.save(newPath)


def load_model():
    model = torch.hub.load('./yolov5/', 'custom', path='yolov5/best.pt', source='local')
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5005, type=int, help="port number")
    args = parser.parse_args()
    model = load_model()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
