from modules import app, cbpi
from thread import start_new_thread
import logging
import time
import requests

prowl_token = None

def prowlToken():
	global prowl_token
	prowl_token = cbpi.get_config_parameter("prowl_token", None)
	if prowl_token is None:
		try:
			cbpi.add_config_parameter("prowl_token", "", "text", "Prowl API Token")
		except:
			cbpi.notify("Prowl Error", "Unable to update database. Update CraftBeerPi and reboot.", type="danger", timeout=None)

@cbpi.initalizer(order=9000)
def init(cbpi):
	cbpi.app.logger.info("INITIALIZE Prowl PLUGIN")
	prowlToken()
	if prowl_token is None or not prowl_token:
		cbpi.notify("Prowl Error", "Check Prowl API Token is set", type="danger", timeout=None)

@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
	prowlData = {}
	prowlData["apikey"] = prowl_token
	prowlData["application"] = "CraftBeerPi3"
	prowlData["event"] = message["message"]
	prowlData["description"] = message["headline"]
	requests.post("https://api.prowlapp.com/publicapi/add", data=prowlData)
