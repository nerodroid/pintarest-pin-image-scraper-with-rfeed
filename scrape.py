import requests
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import itertools
import json
from lxml import etree
import sys
import datetime
from rfeed import *


driver = webdriver.Chrome("chromedriver.exe")
email = ""
password = ""
login_data = []


def json_file():
    try:
        with open('data.txt') as json_file:
            data = json.load(json_file)
            for p in data['login_data']:
                email = p['email']
                login_data.append(p['email'])
                password = p['password']
                login_data.append(password)

    except:
        pass


def login():
    driver.get('https://www.pinterest.com/login/')
    login = driver.find_element_by_id('email')

    login.send_keys(login_data[0])
    login = driver.find_element_by_id('password')
    login.send_keys(login_data[1])
    login_but = driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()
    time.sleep(3)
    print("Login Success")

def scrape_page():
    with open('board_input_list.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:

            final_list = []
            board_name = row[0].split("/")[4]



            print ("board :"+board_name)


            driver.get(row[0])
            try:
                scroll_count =int(row[1])
            except:
                scroll_count=10


            for x in  range(0,0):

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                print(x)
                time.sleep(4)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source,"lxml")
            item_list =soup.find_all("div",{"class":"Grid__Item"})
           # time.sleep(3)



            for k in item_list:
                img = ""
                desc = ''
                scraped_img = (k.find('img')["src"])
                scraped_desc = (k.find('p', {"data-test-id": "desc"}).text)
                post_url = "https://www.pinterest.com" + k.find('div', {'class': 'GrowthUnauthPinImage'}).a['href']
                # tags =  (k.find('div',{"data-test-id":"vasetags"}).text)
                # print (tags)
                #print( [scraped_desc ,scraped_img])

                item = etree.Element('item')

                desc = etree.Element('desc')
                desc.text = scraped_desc
                item.append(desc)

                img = etree.Element('img')
                img.set("src", scraped_img)
                item.append(img)

                item1 = Item(
                    title=scraped_desc,
                    link=scraped_img,

                    description=scraped_desc,
                    pubDate=datetime.datetime.now())

                final_list.append(item1)


                # pretty string
                #s = etree.tostring(item, pretty_print=True)
                #print(s)

                #et = etree.ElementTree(item)

                #et.write(f, pretty_print=True)
            feed = Feed(
                title="Pintarest Rss",
                link=row[0],
                description="Pintarest Rss",
                language="en-US",
                lastBuildDate=datetime.datetime.now(),
                items=final_list)

            with open(board_name+'.xml', 'w', encoding="utf-8") as f:
                f.write(feed.rss())
                time.sleep(1)
            print (feed.rss())

    driver.close()


json_file()
#login()
scrape_page()


