# Libraries / Modules
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import threading
import requests
import json
import logging
import time

# Limits, do no spam this endpoint
app = Flask(__name__)


# turn off logging in output logs (no http post prints)
log = logging.getLogger('werkzeug')
log.disabled = True


# Webhook routing api
@app.route("/api/webhooks/<id>/<str>", methods = ["POST"])
def proxy(id, str):
  
  data = request.get_json(force = True)
  response = requests.post("https://discord.com/api/webhooks/"+id+"/"+str, json = data)
  return "", int(response.status_code)

# Run application
if __name__ == "__main__":
  app.run()