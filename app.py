from flask import Flask,render_template,redirect,url_for,request
#from flask_mail import Mail, Message
from email.message import EmailMessage
from dotenv import load_dotenv
import json
import os
import ssl
import smtplib

app = Flask(__name__)       # create flask app

load_dotenv()               # load enviroment
information:dict = {}       # store configuration setting on json file

# configuration setting for sending email
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

# load the configuration and information data from json file 
def load_information() -> dict:
    with open("information/information.json",'r') as file:
        return json.load(file)
    
    return {}

# page and route for any kind of error that will occur
@app.route('/error',methods=['GET'])
def error(message:str ="",description:str = ""):
    m = request.args.get('message',message)             # temporary storage for message
    d = request.args.get('description',description)     # temporary storage for description
    error = {"message":m,"description":d}               # create error dictionary
    information = load_information()                    # load information from json file
    return render_template('404.html',
                           information = information, 
                           error=error)
    
@app.route('/send_email', methods=['POST'])
def send_email():

    # create secure connection with server and send email
    context = ssl.create_default_context()

    # get form data from request object
    # store data from config that will use
    # to send email later
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
        # try to login to google account and send email
        # then redirect to the home page
        with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'], context=context) as server:
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(email_message)
        return redirect(url_for('index'))
    except Exception as e:
        # if failed to send email it
        # redirect to the 404 page
        return redirect(url_for('error',
                                message="Oops! Email Didn’t Take Off",
                                description="Email failed (Error 500). Please try again later or contact support."))

# main page route
@app.route("/", methods = ['GET','POST'])
def index():
    information = load_information()
    return render_template('index.html',
                           information = information)


if __name__ == '__main__':
        app.run(debug=False)