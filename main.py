import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()
    audio = "Hello. Thanks for your call. I'm ready to take your order."
    resp.say(audio, voice="male")
    resp.record()
    resp.hangup()

    return str(resp)


@app.route("/sms", methods=["POST"])
def sms():
    resp = MessagingResponse()
    message_body = request.form["Body"]
    resp.message(
        f"Welcome to my app. You just sent me a message '{message_body}'."
    )
    return str(resp)


@app.route("/")
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST"), port=os.environ.get("APP_PORT"))
