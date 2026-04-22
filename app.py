from flask import Flask,render_template,redirect,url_for,request,current_app
#from flask_mail import Mail, Message
from email.message import EmailMessage
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import json
import os
import ssl
import smtplib

app = Flask(__name__)       # create flask app

load_dotenv()               # load enviroment
information:dict = {}       # store configuration setting on json file

# validator for the fields in 
# in the form in the page
class FORM(FlaskForm):
    email:EmailField = EmailField('Email', validators=[DataRequired(),Email()])
    name:StringField = StringField("Name", validators=[DataRequired()])
    subject:StringField = StringField("Subject", validators=[DataRequired()])
    message:TextAreaField = TextAreaField("Message", validators=[DataRequired()])


# configuration setting for sending email

# secret key for crft
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# port and server config
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))

# account credential config
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')

# default account to send email config
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# connection config
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')

# other config
app.config['MAIL_DEBUG'] = os.environ.get('MAIL_DEBUG')
app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER')
app.config['TESTING'] = os.environ.get('TESTING')
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND')

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

# check the sending email and will
# response if sending is success
def can_send_email(message:EmailMessage) -> bool:
    
    # create secure connection with server and send email
    context = ssl.create_default_context()
    
    try:
        # try to login to google account and send email
        # then redirect to the home page
        with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'], context=context) as server:
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            server.send_message(message)
            
        return True
    
    except Exception as e:
        print(str(e))
    
    return False
    

# set the email config that needed for sending
# email thru gmail
def set_email(form:FORM) -> EmailMessage:

    sender = current_app.config['MAIL_SENDER']
    receiver = current_app.config['MAIL_RECEIVER'] 
    
    # get form data from request object
    # store data from config that will use
    # to send email later
    name = form.name.data
    email = form.email.data

    subject = f"New Message(Portfolio) from {email} | Subject: {form.subject.data}"
    body = f'Email:{email} \r\n Name:{name} \r\n Message:{form.message.data}'
    
    # create email message and set headers
    email_message = EmailMessage()
    email_message['Subject'] = subject
    email_message['From'] = sender
    email_message['To'] = receiver
    email_message.set_content(body)
    
    return email_message
    

# main page route
@app.route("/", methods = ['GET','POST'])
def index():

    form = FORM()                           # form validator & template
    information = load_information()        # load information from information.js
    
    
    print(form.errors)
    
    # check if the form is submitted 
    # and the form's field is not empty
    if form.validate_on_submit():

        if can_send_email(message=set_email(form)):
            # redirect to home page when sending email is success
            return redirect(url_for('index')) 
        else:
            # if failed to send email it
            # redirect to the 404 page
            return redirect(url_for('error',
                                    message="Oops! Email Didn’t Take Off",
                                    description="Email failed (Error 500). Please try again later or contact support."))
    
    return render_template('index.html',
                           information = information,form=form)


if __name__ == '__main__':
        app.run(debug=False)