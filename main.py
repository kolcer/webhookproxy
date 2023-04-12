# Libraries / Modules
from flask import Flask, request

import requests
import os
import logging
import json

app = Flask(__name__)


# turn off logging in output logs (no http post prints, as they include password)
#log = logging.getLogger('werkzeug')
#log.disabled = True

# Webhook routing api
@app.route("/api/<password>/<id>/<str>", methods = ["POST"])
def proxy(password,id, str):
 
  if password != os.environ['WEBHOOK_PASSWORD']:
    return "", 403 # forbidden
  

  data = request.get_json(force = True)
  print(json.loads(data)['EventType'])

  response = requests.post("https://discord.com/api/webhooks/"+id+"/"+str, json = data)
  return "", int(response.status_code)

# Run application
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])