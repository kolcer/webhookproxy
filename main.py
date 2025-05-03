# Libraries / Modules
from flask import Flask, request

import requests
import os
import logging
import redis

# Set up the data base
db = redis.from_url(os.environ.get("REDIS_PRIVATE_URL"))

app = Flask(__name__)

GAMES = {
  "2418401851": "Crazy Stairs + VR",
  "9585919093": "Kingdoms of Fodienda",
}

# turn off logging in output logs (no http post prints, as they include password)
log = logging.getLogger('werkzeug')
log.disabled = True

# Webhook routing api
@app.route("/api/<password>/<id>/<string>", methods = ["POST"])
def proxy(password,id, string):
 
  if password != os.environ['WEBHOOK_PASSWORD']:
    return "", 403 # forbidden
  

  data = request.get_json(force = True)

  if 'NotificationId' in data:
    newData = {
      'username': data['EventType'],
      'content': '\n'
    }

    for i, v in data['EventPayload'].items():
      if i == "GameIds":
        for k, game in GAMES.items():
          if k in str(v):
            newData['content'] += game + '\n'
      else:
        newData['content'] += i + ': ' + str(v) + '\n\n'

    data = newData

  elif 'climbs' in data:
    #id is discord id and string is a token
    key = "USER_" + str(id)

    #check token
    if db.hget(key,'token').decode('utf-8') != string:
      return "", 403 #wrong token
    
    #climbs
    for alignment, amount in data['climbs'].items():
      db.hset(key,alignment + "_climbs",amount)

    #classic
    for alignment, record in data['records']['classic'].items():
      db.hset(key,alignment + "_classic",record)
   
    #pro
    for alignment, record in data['records']['pro'].items():
      db.hset(key,alignment + "_pro",record)

    #infinite
    for alignment, record in data['records']['infinite'].items():
      db.hset(key,alignment + "_infinite",record)
  
    print('success')
    return "", 200 #success

  response = requests.post("https://discord.com/api/webhooks/"+id+"/"+string, json = data)
  return "", int(response.status_code)

# Run application
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])
