# Libraries / Modules
from flask import Flask, request

import requests
import os
import logging
import json
from datetime import datetime

app = Flask(__name__)


# turn off logging in output logs (no http post prints, as they include password)
#log = logging.getLogger('werkzeug')
#log.disabled = True

# Webhook routing api
@app.route("/api/<password>/<id>/<string>", methods = ["POST"])
def proxy(password,id, string):
 
  if password != os.environ['WEBHOOK_PASSWORD']:
    return "", 403 # forbidden
  

  data = request.get_json(force = True)

  if 'NotificationId' in data:
    newData = {
      'username': data['EventType'],
      'content': datetime.strptime(data['EventTime'],'%Y-%m-%dT%H::%M::%S.%f%Z') + '\n\n'
    }

    for i, v in data['EventPayload'].items():
      newData['content'] += i + ': ' + str(v) + '\n\n'
     

  response = requests.post("https://discord.com/api/webhooks/"+id+"/"+string, json = data)
  return "", int(response.status_code)

# Run application
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])