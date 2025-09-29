from flask import Flask,render_template,url_for,jsonify,request
from flask_mail import Mail, Message
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)
information:dict = {}

load_dotenv()

# config for email sending
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_DEFAULT_SENDER'] = ('<your name sender>', '<your-email>@gmail.com')

mail = Mail(app)

def load_information() -> dict:
    with open("information/information.json",'r') as file:
        return json.load(file)
    
    return {}

""" @app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    subject = data.get('title')
    recipient = data.get('email')   # single recipient
    body = data.get('message')

    if not subject or not recipient or not body:
        return jsonify({"message": "The fields title, email, and message are required"}), 400

    msg = Message(
        subject=subject,
        recipients=[recipient],  # still needs to be a list
        body=body
    )
    mail.send(msg)

    return jsonify({"message": "Email sent successfully"}), 200 """

    

@app.route("/", methods = ['GET','POST'])
def index():
    information = load_information()
    return render_template('index.html',information = information)


if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)