#!/usr/bin/env python
# coding: utf-8

# In[22]:


import requests
import time
from datetime import datetime


# In[23]:


url = 'http://127.0.0.1:5000/messages'
after_id = -1


# In[24]:


def pretty_print(message):
    '''
    2020/09/08 10:00:23 Name
    Text
    
    '''
    dt = datetime.fromtimestamp(message['timestamp'])
    dt = dt.strftime('%Y/%m/%d %H:%M:%S')
    first_line = dt + '  ' + message['name']
    print(first_line)
    print(message['text'])
    print()


# In[25]:


while True:
    response = requests.get(url, params={'after_id': after_id})
    messages = response.json()['messages']
    for message in messages:
        pretty_print(message)
        after_id = message['id']
    time.sleep(1)

