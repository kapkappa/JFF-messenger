#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests


# In[ ]:


url = 'http://127.0.0.1:5000/send'

name = input('Введи имя: ')
while True:
    text = input()
    data = {'name' : name, 'text' : text}
    response = requests.post(url, json=data)

