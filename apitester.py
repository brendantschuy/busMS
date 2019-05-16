import requests as rq
import time
import yaml

# strings file (YAML format) initialization
strings = yaml.load(open("strings.txt", "r"))


def getResponse(id):
    return rq.get("https://developer.trimet.org/ws/V1/arrivals/locIDs/" + id + "/appID/" + strings["trimet_app_code"])

def formatResponse(text):
    arrival = text.split("estimated=\"")[1]
    arrival = float(arrival.split("\"")[0])
    arrival = round((arrival/1000 - time.time())/60, 2)
    print(f"Time until arrival: {arrival} minutes.")

def timeUntil(id):
    stop = getResponse(str(id)).text
    formatResponse(stop)
