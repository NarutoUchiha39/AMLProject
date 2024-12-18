import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import keras
from werkzeug.utils import secure_filename
from uuid import uuid4

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
W, H = 256, 256

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
segmentation_model = keras.models.load_model("model.keras", compile=False)

# CORS and Upload Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/upload": {"origins": "*"}})

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
        
        # Generate unique filename
        file_name = f"{str(uuid4())}_{secure_filename(file.filename)}"
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        
        # Save the image
        cv2.imwrite(file_path, infect)
        
        # Return URL (using relative path)
        return jsonify({"image_url": f"http://localhost:5000/uploads/{file_name}"}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)