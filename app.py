import io
import os
import json
import torch

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import *  

upload_folder = os.path.join('static', 'upload')


app = Flask(__name__)
imagenet_class_index = json.load(open('imagenet_class_index.json'))
model =torch.hub.load("WongKinYiu/yolov7", 'custom', 'yolov7_training.pt')
model.eval()

@app.route('/')  
def main():  
    return render_template("index.html")  
  


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_id': class_id, 'class_name': class_name})


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        img_bytes = f.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return render_template("acknowledgement.html", class_id = class_id, class_name = class_name) 

if __name__ == '__main__':
    app.run()



