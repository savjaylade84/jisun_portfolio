from flask import Flask,render_template,request
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def index() -> None:
    pass


