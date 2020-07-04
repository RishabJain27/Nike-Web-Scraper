# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import json
from pymongo import MongoClient
import sys
import time
sys.stdout = open('file', 'w', encoding="utf-8")


url = "https://www.nike.com/w/new-shoes-3n82yzy7ok"
# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

# get web page
driver.get(url)
# execute script to scroll down the page
driver.maximize_window()
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

#connect to database
client = MongoClient("mongodb+srv://rjain9:Ilikepie16%21@cluster0-wgm3y.mongodb.net/test?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["nike"]
aTagsInLi = driver.find_elements_by_xpath("//div[@class='product-card css-ua5d08 css-z5nr6i css-11ziap1 css-zk7jxt css-dpr2cn product-grid__card ']")
                                                          
line_items=[]
for a in aTagsInLi:
    
    print("here")
    #get div container for image details
    img = a.find_element_by_tag_name('img')
    #get div for site line
    siteDiv = a.find_element_by_tag_name('a')

    #get name of shoe
    name = img.get_attribute('alt')
    #get image url
    image_url = img.get_attribute('src')
    #get site link
    site = siteDiv.get_attribute('href')
    #get category of shoe
    category = a.find_element_by_class_name('product-card__subtitle').text

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

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)

    




