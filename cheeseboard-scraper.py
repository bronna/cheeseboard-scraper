#!/usr/bin/env python
# coding: utf-8

# In[57]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64


# In[59]:


response = requests.get("https://cheeseboardcollective.coop/pizza/")
doc = BeautifulSoup(response.text, 'html.parser')


# In[67]:


# Find out what pizzas are on the menu this week at Cheeseboard Collective in Berkeley
pizzas = doc.select(".pizza-list article")

rows = []

for pizza in pizzas:
    print("-----")
    row = {}
    
    row['date'] = pizza.select_one('.date p').text.strip()
    
    try:
        pizza.select_one('.menu p i').clear()
        row['pizza'] = pizza.select_one('.menu p').text.strip()
    except:
        row['pizza'] = pizza.select_one('.menu p').text.strip()
    
    print(row)
    
    rows.append(row)


# In[68]:


df = pd.DataFrame(rows)
df


# In[71]:


df.to_csv('cheeseboard-menu.csv', index=False)


# In[ ]:


message = Mail(
    from_email=os.environ.get('FROM_EMAIL'),
    to_emails=os.environ.get('TO_EMAIL'),
    subject='See the Cheeseboard menu for this week',
    html_content="Pizzas are... attached.")

# https://www.twilio.com/blog/sending-email-attachments-with-twilio-sendgrid-python
with open('cheeseboard-menu.csv', 'rb') as f:
    data = f.read()
    f.close()
encoded_file = base64.b64encode(data).decode()

attachedFile = Attachment(
    FileContent(encoded_file),
    FileName('cheeseboard-menu.csv'),
    FileType('text/csv'),
    Disposition('attachment')
)
message.attachment = attachedFile

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
