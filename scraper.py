# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import json
from pymongo import MongoClient
import sys
sys.stdout = open('file', 'w', encoding="utf-8")


url = "https://www.nike.com/w/new-shoes-3n82yzy7ok"
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

# get web page
driver.get(url)
# execute script to scroll down the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#connect to database
client = MongoClient("mongodb+srv://<username>:<password>@cluster0-wgm3y.mongodb.net/test?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["nike"]

#find every div with class name
aTagsInLi = driver.find_elements_by_class_name('product-card__img-link-overlay')
line_items=[]
for a in aTagsInLi:
    #print(a.get_attribute('href'))
    img = a.find_element_by_tag_name('img')

    myjson3 = {
                'name': img.get_attribute('alt'),
                'image_url': img.get_attribute('src'),
                'site': a.get_attribute('href')
            }
    line_items.append(myjson3)
    #print("img link: ", img.get_attribute('src'), " name: ", img.get_attribute('alt'))

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)

    




