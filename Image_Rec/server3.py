import argparse
import socket
import torch
import json
from PIL import Image
import io

def handle_client_request(conn, addr):
    while True:
        # receive request from client
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == "Test":
            # receive image data size
            image_size = int(conn.recv(1024).decode())
            # receive image data
            image_bytes = b""
            while len(image_bytes) < image_size:
                image_bytes += conn.recv(1024)
            # perform detection
            img = Image.open(io.BytesIO(image_bytes))
            results = model(img, size=640)  # reduce size=320 for faster inference
            # convert detection results to JSON
            results_json = results.pandas().xyxy[0].to_json(orient="records")
            results_json = results_json.encode()
            # send detection results size
            results_size = str(len(results_json)).encode()
            conn.sendall(results_size)
            # send detection results
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
