#!/usr/bin/env python
# coding: utf-8

# In[5]:


import flask
import time
from datetime import datetime


# In[6]:


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
        'users_count' : len(set(message['name'] for message in db)) #another realization
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
    if data['text'].find(PASSWORD_ADD) != -1:
        data['text'] = data['text'].replace(PASSWORD_ADD+' ','')
        BLACK_LIST.append(data['text'])
    
    if data['text'].find(PASSWORD_REM) != -1:
        data['text'] = data['text'].replace(PASSWORD_REM+' ','')
        BLACK_LIST.remove(data['text'])
    
    for word in BLACK_LIST:
        data['text'] = data['text'].replace(word,'*'*len(word))
    
    db.append({
        'id' : len(db),
        'name' : data['name'],
        'text' : data['text'],
        'timestamp' : time.time()
    })
    
        
    return {'OK':True}

@app.route('/messages')
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0
        #after_id = 0
        #return {'all messages' : db[after_id:]}
    
    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit > max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit        
    
    after_id=0  
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        after_id +=1
    return {'messages': db[after_id : after_id + 50]}


app.run()

