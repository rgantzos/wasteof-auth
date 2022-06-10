from replit import db
import requests
import random
import json
from flask import Flask, render_template, jsonify, request
app = Flask('app')

@app.route('/')
def home():
  return render_template('Home.html')

@app.route('/done/')
def done():
  return render_template('Home.html')

@app.route('/generate/')
def generate():
  privateCode = str(random.randint(0, 9999999999))
  publicCode = str(random.randint(0, 9999999999))
  db[privateCode] = publicCode
  return jsonify({"url":f"https://wasteof-auth.rgantzos.repl.co/auth/{privateCode}/", "code":privateCode})

@app.route('/auth/<privateCode>/', methods=['GET'])
def auth(privateCode):
  if privateCode in db:
    return render_template('auth.html', code=db[privateCode], redirect=request.args.get('redirect', None))
  else:
    return('not found')
  

@app.route('/getUser/<privateCode>/')
def getUser(privateCode):
  publicCode = db[privateCode]
  response = requests.get('https://api.wasteof.money/posts/628bde28c370574fae7b6067/comments').text
  data = json.loads(response)
  if data['comments'][0]['content'] == f'<p>{publicCode}</p>':
    return data['comments'][0]['poster']['name']
  else:
    return 'Try again.'

app.run(host='0.0.0.0', port=8080)
