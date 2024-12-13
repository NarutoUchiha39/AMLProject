import os
from flask import Flask,jsonify, redirect, request
from flask_cors import CORS
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.secret_key="Ok"

cors = CORS(app,resources=
            {
                r"/upload":{"origins":"*"}
            }
    )
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.post("/upload")
def upload():
    print(request.method)
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return jsonify({"error":"Not a file!"}),500
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error":"No files selected!"}),500
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"success":"File uploaded!"}),200




if __name__ == "__main__":
    app.run(host="0.0.0.0",port="5000",debug=True)


    