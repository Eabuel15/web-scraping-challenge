#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:

def scrape():
    browser = init_browser()
    mars_dict = {}
# News site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html

    news_soup = bs(html, 'html.parser')


    # In[4]:


    # Retrieve latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    print(news_title)
    print('-----------------------------------------------------')
    print(news_p)


    # In[5]:


    # JPL Mars Space Images - Featured Image


    # In[6]:


    # Mars Image

    images_url = 'https://spaceimages-mars.com/'
    browser.visit(images_url)


    # In[7]:


    image_html = browser.html

    images_soup = bs(image_html, 'html.parser')


    # In[8]:


    relative_image_path = images_soup.find_all('img')[1]['src']
    featured_image_url = images_url + relative_image_path
    print(featured_image_url)


    # In[9]:


    # Mars Facts
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    facts_html = browser.html

    facts_soup = bs(html, 'html.parser')


    # In[10]:


    tables = pd.read_html(facts_url)
    tables


    # In[11]:


    mars_facts_df = tables[1]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df


    # In[12]:


    mars_html_table = mars_facts_df.to_html()
    mars_html_table


    # In[13]:


    mars_html_table.replace('\n', '')


    # In[14]:


    print(mars_html_table)


    # In[15]:


    # Mars Hemispheres
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')


    # In[19]:


    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

# Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(hemispheres_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict)

# print(hemisphere_image_urls)


# In[21]:


    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }


# In[23]:


    return mars_dict


# In[ ]:
