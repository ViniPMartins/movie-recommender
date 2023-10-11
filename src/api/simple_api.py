from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "API Rodando"

@app.route("/api", methods=['POST'])
def api():

    params = request.get_json()
    genres = params['generos']

    message = json.dumps({"message":genres})
    return message

if "__main__" == __name__:
    app.run(debug=True, host='0.0.0.0')