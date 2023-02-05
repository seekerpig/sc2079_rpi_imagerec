import argparse
import io

import torch
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

DETECTION_URL = "/Test"

#flask connection

@app.route("/")
def home():
    return "<h1>Welcome to the HomePage!</h1>"
@app.route(DETECTION_URL, methods=["POST"])


def predict():
    #if not request.method == "POST":
    #    return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=640)  # reduce size=320 for faster inference
        results.save('runs')
        return results.pandas().xyxy[0].to_json(orient="records")
    
        df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
        df_results['bboxWt'] = df_results['xmax'] - df_results['xmin']
        df_results['bboxArea'] = df_results['bboxHt'] * df_results['bboxWt']

        df_results = df_results.sort_values('bboxArea', ascending=True)  # Label with largest bbox height will be last
        print(df_results)
        pred_list = df_results['name'].to_numpy()
        pred = 'NA'
        # This if statement will ignore Bullseye unless they are the only image detected and select the last label in
        # the list (the last label will be the one with the largest bbox height)
        if pred_list.size != 0:
            for i in pred_list:
                if i != 'Bullseye':
                    pred = i
        
        Symbol_Map_to_id = {
            "NA": 'NA',
            "One": 11,
            "Two": 12,
            "Three": 13,
            "Four": 14,
            "Five": 15,
            "Six": 16,
            "Seven": 17,
            "Eight": 18,
            "Nine": 19,
            "A": 20,
            "B": 21,
            "C": 22,
            "D": 23,
            "E": 24,
            "F": 25,
            "G": 26,
            "H": 27,
            "S": 28,
            "T": 29,
            "U": 30,
            "V": 31,
            "W": 32,
            "X": 33,
            "Y": 34,
            "Z": 35,
            "Up": 36,
            "Down": 37,
            "Right": 38,
            "Left": 39,
            "Up Arrow": 36,
            "Down Arrow": 37,
            "Right Arrow": 38,
            "Left Arrow": 39,
            "Stop": 40,
            "Bullseye": 41
        }
        image_id = str(Symbol_Map_to_id[pred])
        
        result = {
            "image_id": image_id
        }

        return jsonify(result)
    
        



        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5005, type=int, help="port number")
    args = parser.parse_args()
    model = torch.hub.load("ultralytics/yolov5","custom",path="best.pt")
    #model = torch.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
    

