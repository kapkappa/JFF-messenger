#!/usr/bin/env python
# coding: utf-8

# In[74]:


import flask
import time
from datetime import datetime


# In[77]:


from flask import Flask
from flask import request

app = Flask(__name__)
db = []
BLACK_LIST=[]
unique_names = [] #Корректно заработает при наличии функции логина/пароля, т.е. созздания акаунта.
PASSWORD_ADD = 'ADD_TO_BLACK_LIST'
PASSWORD_REM = 'REM_FROM_BLACK_LIST'
PASSWORD_SHW = 'SHOW_BIG_BLACK_LIST'

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
    intro = "Добро пожаловать на сервер!<br>"     + "<a href='/status'>Статус</a><br>"     + "<a href='/shutdown'>Shutdown</a><br>"     + "<a href='/messages'>Messages</a><br>"     + "<a href='/send'>Send</a>"
    return intro

@app.route("/status")
def status():
    dn = datetime.now()
    info = ''
    st = {
        'Status' : True,
        'Name' : 'Messenger',
        'Time' : dn.strftime('%d.%m.%Y %H:%M:%S'),
        'Num of messages' : len(db),
        'Num of Users' : len(unique_names),
    }
    for (key, value) in st.items():
        info = info + '<pre>' + '{:<20}'.format(str(key)) + str(value) + '</pre>'
    return info

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    if data['name'] not in unique_names:
        unique_names.append(data['name'])
    
    if data['text']==PASSWORD_SHW:
        db.append({
            'id' : len(db),
            'name' : 'admin',
            'text' : BLACK_LIST,
            'timestamp' : time.time()
        })
    else:
        if data['text'].find(PASSWORD_ADD) != -1:
            data['text'] = data['text'].replace(PASSWORD_ADD+' ','')
            BLACK_LIST.append(data['text'])
    
        if data['text'].find(PASSWORD_REM) != -1:
            data['text'] = data['text'].replace(PASSWORD_REM+' ','')
            BLACK_LIST.remove(data['text'])
    
        for word in BLACK_LIST:
            data['text'] = data['text'].replace(word,'***')
    
        db.append({
            'id' : len(db),
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
        return {'all messages' : db[after_id:]}
    return {'messages': db[after_id : min(after_id + 50, len(db))]}


# In[78]:


app.run()

