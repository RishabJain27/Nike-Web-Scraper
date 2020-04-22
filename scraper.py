# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import json
from pymongo import MongoClient


url = "https://www.nike.com/w/new-shoes-3n82yzy7ok"
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

# get web page
driver.get(url)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#connect to database
client = MongoClient("mongodb+srv://<user>:<password>@cluster0-wgm3y.mongodb.net/test?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["nike"]

#find all img tags and take out unnecessary 
aTagsInLi = driver.find_elements_by_css_selector('img')
aTagsInLi.pop()
aTagsInLi.pop()
del aTagsInLi[0:2] 

#array for json objects
line_items=[]
#loop through all elements found and add them to array
for a in aTagsInLi:
    myjson3 = {
                'name': a.get_attribute('alt'),
                'image_url': a.get_attribute('src'),
            }

    str = a.get_attribute('alt')
    if str.find("Shoe") > 0:
    	line_items.append(myjson3)
    	
    #print("img link: ", a.get_attribute('src'), " name: ", a.get_attribute('alt'))

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)


    




