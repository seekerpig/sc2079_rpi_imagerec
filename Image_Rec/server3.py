import argparse
import io
from ultralytics import YOLO
import torch
from flask import Flask, request
from PIL import Image


model = YOLO('MDP.pt')

app = Flask(__name__)

DETECTION_URL = "/Test"

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
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5010, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
    

