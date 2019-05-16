#/usr/bin/env python
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests as rq
import time
from keys import trimet_key

#def __init__():
#    importlib.import_module("keys")

app = Flask(__name__)
#strings = yaml.load(open("strings.txt", "r"))

def getResponse(id):
    #return rq.get("https://developer.trimet.org/ws/V1/arrivals/locIDs/" + id + "/appID/" + strings["trimet_app_code"])
    return rq.get("https://developer.trimet.org/ws/V1/arrivals/locIDs/" + id + "/appID/" + trimet_key)

def formatResponse(text):
    arrival = text.split("estimated=\"")[1]
    arrival = float(arrival.split("\"")[0])
    arrival = str(round((arrival/1000 - time.time())/60, 2))
    responseMsg = "Time until arrival: " + arrival + "minutes."
    return responseMsg

def timeUntil(id):
    stop = getResponse(str(id)).text
    return formatResponse(stop)

@app.route("/sms", methods=['GET', 'POST'])
def trackerReply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response

    body = request.values.get('Body')

    resp = MessagingResponse()

    # Add a message
    stopId = int(body)
    stopMsg = timeUntil(stopId)
    resp.message(stopMsg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


