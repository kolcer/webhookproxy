# Libraries / Modules
from flask import Flask, request

import requests
import os


app = Flask(__name__)


# Webhook routing api
@app.route("/api/<password>/<id>/<str>", methods = ["POST"])
def proxy(password,id, str):
 
  if password != os.environ['WEBHOOK_PASSWORD']:
    print('old server')
  else:
    print('new server')

  data = request.get_json(force = True)
  response = requests.post("https://discord.com/api/webhooks/"+id+"/"+str, json = data)
  return "", int(response.status_code)

# Run application
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])