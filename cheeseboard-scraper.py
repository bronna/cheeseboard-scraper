#!/usr/bin/env python
# coding: utf-8

# In[57]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


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


df.to_csv('cheeseboard-menu.csv')


# In[ ]:




