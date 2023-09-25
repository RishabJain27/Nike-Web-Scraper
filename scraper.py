# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from pymongo import MongoClient
import sys
import time
sys.stdout = open('file', 'w', encoding="utf-8")

# get web page
url = "https://www.nike.com/w/new-shoes-3n82yzy7ok"
driver = webdriver.Firefox()
driver.get(url)

# execute script to scroll down the page
driver.maximize_window()
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#connect to database
client = MongoClient("mongodb+srv://rjain9:Ilikepie16@sneakers.1azjgzw.mongodb.net/?retryWrites=true&w=majority")

db = client["Shoes"]
mycol = db["nike"]
aTagsInLi = driver.find_elements("xpath", "//div[@class='product-card product-grid__card  css-1t0asop']")
                                                          
line_items=[]
categoryCounter = 0
for a in aTagsInLi:
    
    #get div container for image details
    img = a.find_element(By.TAG_NAME,'img')
    #get div for site line
    siteDiv = a.find_element(By.TAG_NAME, 'a')

    #get name of shoe
    name = img.get_attribute('alt')
    #get image url
    image_url = img.get_attribute('src')
    #get site link
    site = siteDiv.get_attribute('href')
    #get category of shoe
    category = a.find_elements("xpath", "//div[@class='product-card__subtitle']")[categoryCounter].text

    #determine gender
    if "Men" in category:
        gender = "Male"
    elif "Women" in category:
        gender = "Female"
    elif "Kid" in category or "Baby" in category or "Toddler" in category:
        gender = "Kid"
    else:
        gender = "Unisex"

    #create json object for database
    myjson3 = {
                'name': name,
                'image_url': image_url,
                'site': site,
                'category': category,
                'gender': gender,
                'brand' : 'Nike'
            }
    print(myjson3)
    line_items.append(myjson3)
    categoryCounter = categoryCounter + 1

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)