from flask import Flask,jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app,resources=
            {
                r"*":{"origins":"*"}
            }
    )

@app.route("/")
def home():
    return jsonify({"name":"/"})




if __name__ == "__main__":
    app.run(host="0.0.0.0",port="5000",debug=True)


    