import os
import openai
import uuid

from langchain.adapters import openai as lc_openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/voice", methods=["POST"])
def voice():
    menu = """
    pepperoni pizza  12.95, 10.00, 7.00 \
    cheese pizza   10.95, 9.25, 6.50 \
    eggplant pizza   11.95, 9.75, 6.75 \
    fries 4.50, 3.50 \
    greek salad 7.25 \
    Toppings: \
    extra cheese 2.00, \
    mushrooms 1.50 \
    sausage 3.00 \
    canadian bacon 3.50 \
    AI sauce 1.50 \
    peppers 1.00 \
    Drinks: \
    coke 1.00, 2.00, 3.00 \
    sprite 3.00, 4.00, 5.00 \
    bottled water 5.00 \
    """

    instruction =  """
    You are OrderBot, an automated service to collect orders for a pizza restaurant. \
    You first greet the customer, then collects the order, \
    and then ask if it's a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    Finally you collect the payment.\
    If it's a delivery, you ask for an address. \
    Make sure to clarify all options, extras and sizes to uniquely \
    identify the item from the menu.\
    You respond in a short, very conversational friendly style. \
    The menu includes \
    """

    conversation = [
        {"role": "system", "content": f"""{instruction}{menu}""" },
        {"role": "user", "content": "hi"}  # This makes the API complete for one turn.
    ]

    client = openai.OpenAI()
    resp = VoiceResponse()
    audio = "Hello. Thanks for your call. I'm ready to take your order."
    resp.say(audio, voice="male")
    response = lc_openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=0  # Try to as deterministic as possible.
    )
    reply = response['choices'][0]['message']['content']
    resp.say(reply, voice="male")


    # resp.record()
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
