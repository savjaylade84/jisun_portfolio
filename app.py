from flask import Flask,render_template,redirect,url_for,request
#from flask_mail import Mail, Message
from email.message import EmailMessage
from dotenv import load_dotenv
import json
import os
import ssl
import smtplib

app = Flask(__name__)
load_dotenv()
information:dict = {}

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_DEBUG'] = os.environ.get('MAIL_DEBUG')
app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER')
app.config['TESTING'] = os.environ.get('TESTING')
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND')


#mail = Mail(app)


def load_information() -> dict:
    with open("information/information.json",'r') as file:
        return json.load(file)
    
    return {}

    
@app.route('/send_email', methods=['POST'])
def send_email():

    # create secure connection with server and send email
    context = ssl.create_default_context()

    # get form data from request object
    name = request.form.get('name', 'No Name')
    email = request.form.get('email', 'No Email')
    subject = f"New Message(Portfolio) from {email} | Subject: {request.form.get('subject', 'No Subject')}"
    sender = app.config['MAIL_SENDER']
    receiver = app.config['MAIL_RECEIVER']
    body = f'Email:{email} \r\n Name:{name} \r\n Message:{request.form.get('message', '')}'

    # create email message and set headers
    email_message = EmailMessage()
    email_message['Subject'] = subject
    email_message['From'] = sender
    email_message['To'] = receiver
    email_message.set_content(body)

    try:
        with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], context=context) as server:
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(email_message)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error sending email: {e}")
        return "Failed to send email", 500


@app.route("/", methods = ['GET','POST'])
def index():
    information = load_information()
    return render_template('index.html',information = information)


if __name__ == '__main__':
        app.run(debug=True)