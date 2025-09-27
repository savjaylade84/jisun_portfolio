from flask import Flask,render_template,url_for
import json
import os

app = Flask(__name__)
information:dict = {}

def load_information() -> dict:
    with open("information/information.json",'r') as file:
        return json.load(file)
    
    return {}

@app.route("/", methods = ['GET','POST'])
def index():
    information = load_information()
    return render_template('index.html',information = information)


if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)