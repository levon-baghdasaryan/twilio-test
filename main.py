import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/sms", methods=["POST"])
def sms():
    resp = MessagingResponse()
    message_body = request.form['Body']
    resp.message(f"Welcome to my app. You just sent me a message '{message_body}'.")
    return str(resp)


@app.route("/")
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST"), port=os.environ.get("APP_PORT"))
