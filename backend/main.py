import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import keras
import torch
import torchvision
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
W, H = 256, 256

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Keras model
segmentation_model = keras.models.load_model("model.keras", compile=False)
categories = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

def create_models():
    # Create and load pretrained models (VGG19 and ResNet50)
    resnet = torchvision.models.resnet50()
    vgg19 = torchvision.models.vgg19()

    num_ftrs = resnet.fc.in_features
    resnet.fc = torch.nn.Linear(num_ftrs, 7)

    num_ftrs_ = vgg19.classifier[6].in_features
    vgg19.classifier[6] = torch.nn.Linear(num_ftrs_, 7)

    resnet_model_weights = torch.load("resnet_pret.pth", map_location=torch.device("cpu"))
    vgg19_model_weights = torch.load("vgg19_pret.pth", map_location=torch.device("cpu"))

    resnet.load_state_dict(resnet_model_weights)
    vgg19.load_state_dict(vgg19_model_weights)

    return [vgg19, resnet]

# CORS and Upload Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/upload": {"origins": "*"}})
models = create_models()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_image(img):
    x = cv2.resize(img, (W, H))
    x = x / 255.0
    x = x.astype(np.float32)
    return x

def extract_infected_area(image, mask):
    mask = (mask > 0.5).astype(np.uint8)
    infected_area = image * mask
    return infected_area

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Not a file!"}), 500

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No files selected!"}), 500

    if file and allowed_file(file.filename):
        img_np = np.frombuffer(file.stream.read(), np.uint8)
        img_np = cv2.imdecode(img_np, cv2.IMREAD_COLOR)  # Read the image as a numpy array

        test_x_image = read_image(img_np)
        test_x_image = np.expand_dims(test_x_image, axis=0)

        # Predict using the segmentation model
        res = segmentation_model.predict(test_x_image)
        res_image = np.squeeze(res)
        res_image = np.expand_dims(res_image, axis=-1)

        # Extract the infected area
        infect = extract_infected_area((test_x_image * 255).astype(np.uint8), res_image)
        infect = np.squeeze(infect)

        res_vgg19 = models[0].eval()
        res_resnet = models[1].eval()
        pred_resnet = None
        pred_vgg19 = None
        conf_resnet = None
        conf_vgg19 = None

        with torch.no_grad():
            infect_ = infect.astype(np.float32)
            infect_ = np.expand_dims(infect_, axis=0)
            torch_image = torch.from_numpy(infect_)
            torch_image = torch_image.permute(0, 3, 1, 2)

            # VGG19 Prediction
            vgg19_output = res_vgg19(torch_image)
            conf_vgg19, predicted_idx_vgg19 = torch.max(vgg19_output, dim=1)
            pred_vgg19 = categories[predicted_idx_vgg19.item()]
            conf_vgg19 = torch.softmax(vgg19_output, dim=1).max().item()  # Get confidence

            # ResNet Prediction
            resnet_output = res_resnet(torch_image)
            conf_resnet, predicted_idx_resnet = torch.max(resnet_output, dim=1)
            pred_resnet = categories[predicted_idx_resnet.item()]
            conf_resnet = torch.softmax(resnet_output, dim=1).max().item()  # Get confidence

        # Generate unique filename
        file_name = f"{str(uuid4())}_{secure_filename(file.filename)}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Save the image
        cv2.imwrite(file_path, infect)

        # Return URL, predictions, and confidence
        return jsonify({
            "image_url": f"http://localhost:5000/uploads/{file_name}",
            "predictions": [pred_vgg19, pred_resnet],
            "confidence": [conf_vgg19, conf_resnet]
        }), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
