import argparse
import io
import cv2
import torch
import socket
from PIL import Image

DETECTION_PORT = 5005
DETECTION_URL = "/Test"

def handle_client_request(conn, addr):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        if data == DETECTION_URL.encode():
            # receive image data
            image_size = int(conn.recv(1024).decode())
            image_bytes = b""
            while len(image_bytes) < image_size:
                image_bytes += conn.recv(1024)
            # perform detection
            img = Image.open(io.BytesIO(image_bytes))
            results = model(img, size=640)  # reduce size=320 for faster inference
            results.save('runs')
            # send detection results back to client
            results_json = results.pandas().xyxy[0].to_json(orient="records")
            results_json = results_json.encode()
            results_size = str(len(results_json)).encode()
            conn.sendall(results_size)
            conn.sendall(results_json)
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket server exposing YOLOv5 model")
    parser.add_argument("--port", default=5005, type=int, help="port number")
    args = parser.parse_args()
    model = torch.hub.load("ultralytics/yolov5","custom",path="best1.pt")
    #model = torch.load("ultralytics/yolov5", "yolov5s", force_reload=True)  # force_reload to recache
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", args.port))
    server.listen(5)
    print("Socket server started on port", args.port)
    while True:
        conn, addr = server.accept()
        print("Accepted connection from", addr)
        handle_client_request(conn, addr)
