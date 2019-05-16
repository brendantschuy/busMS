from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests as rq
import time
from keys import trimet_key

app = Flask(__name__)

#API request
def getResponse(id):
    return rq.get("https://developer.trimet.org/ws/V1/arrivals/locIDs/" + id + "/appID/" + trimet_key)

#Format response
def formatResponse(text):
    arrival = text.split("estimated=\"")[1]
    arrival = float(arrival.split("\"")[0])
    arrival = str(round((arrival/1000 - time.time())/60, 2))
    responseMsg = "Time until arrival: " + arrival + "minutes."
    return responseMsg

#Driver
def timeUntil(id):
    stop = getResponse(str(id)).text
    return formatResponse(stop)

#Interacts w/ SMS:
@app.route("/sms", methods=['GET', 'POST'])
def trackerReply():
    body = request.values.get('Body')

    resp = MessagingResponse()

    stopId = int(body)
    stopMsg = timeUntil(stopId)
    resp.message(stopMsg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


