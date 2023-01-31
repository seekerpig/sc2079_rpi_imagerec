from server import *
import os 
import shutil
import time
import glob
import torch
from PIL import Image


def load_model():
    model = torch.hub.load('./', 'custom', path='best.pt', source='local')
    return model

def predict_image(image, model):
    img = Image.open(os.path.join('uploads', image))
    result = model(img)
    results.save('runs')
    return result