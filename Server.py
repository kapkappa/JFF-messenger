#!/usr/bin/env python
# coding: utf-8

# In[24]:


import flask
import time
from datetime import datetime


# In[64]:


from flask import Flask
from flask import request

app = Flask(__name__)
db = []

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route("/")
def hello():
    return """Добро пожаловать на сервер!
    <a href='/status'>Статус</a>
    <a href='/shutdown'>Shutdown</a>
    <a href='/messages'>Messages</a>"""

@app.route("/status")
def status():
    dn = datetime.now()
    st = {
        'Status' : True,
        'Name' : 'Messenger',
        'Time' : dn.strftime('%d.%m.%Y %H:%M:%S')
    }
    return st

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    
    db.append({
        'id' : len(db), #Идентификатор - размер базы данных, т.е. номер элемента в базе данных
        'name' : data['name'],
        'text' : data['text'],
        'timestamp' : time.time()
    })
    return {'OK':True}

@app.route('/messages')
def messages():
    if 'after_id' in request.args:
        after_id = int(request.args['after_id']) + 1
    else:
        after_id = 0
    
    return {'messages': db[after_id:]}


# In[65]:


app.run(debug=False)

