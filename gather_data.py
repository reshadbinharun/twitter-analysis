#reference: https://dev.to/swyx/scraping-my-twitter-social-graph-with-python-and-selenium--hn8
#%matplotlib inline NORE: for Jupyter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re
from bs4 import BeautifulSoup as bs
from dateutil import parser
import pandas as pd
import itertools
import matplotlib.pyplot as plt

# to allow login for twitter:
# https://gist.github.com/momota10/969d904b4cad239da2a5c00df1ad87e7
from getpass import getpass

driver = webdriver.Firefox()
driver.get("https://twitter.com/login")

##HELPER FUNCTIONS

def login_twitter(driver, username, password):

    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")

    username_field.send_keys(username)
    # driver.implicitly_wait(1)
    
    password_field.send_keys(password)
    # driver.implicitly_wait(1)

    driver.find_element_by_class_name("EdgeButtom--medium").click()

def scrollAndGather(driver, scrolls):
    for i in range(1,scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrollTO takes x-coord and y-coord as inputs
        time.sleep(2) # wait for page to load
        #gather
        print(i)

def inputTag(driver, tag):
    searchBox = driver
    searchBox.find_element_by_xpath("//*[@id=\"search-query\"]").send_keys(tag)
    searchBox.find_element_by_xpath("//*[@id=\"global-nav-search\"]/span/button").click()
    searchBox.implicitly_wait(2) # wait for load
    return searchBox

#FireFox's xpath seem to be indexed slightly differently from Chrome's
def FingFer(driver):
    while True:
        choice = int(input("Get data on following (1) or followers (2)? Enter integer input please. "))
        if choice == 1:
            following = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a")
            link = following.get_attribute("href")
            count = int(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a/span[2]").get_attribute("data-count"))
            print("This tag has {} following.".format(count))
            driver.get(link)
            break
        elif choice == 1:
            followers = driver.find_element_by_xpath("")
            break
        else:
            print("Please enter either 1 or 2\n")
    return


#HELPER FUNCTIONS

#USER INPUTS:
#COMMENTED OUT FOR TEST MODE:
# tag_input = input("What tag would you want to search? ")
# scrolls = int(input("How many scrolls would you like to do? "))
tag_input = "Galatea Surgical"
scrolls = 10

if __name__ == "__main__":
    ##COMMMENTED OUT FOR TEST MODE
    # username = input("user name : ")
    # password = getpass("password  : ")
    username = "reshadbinharun"
    password = "Ree*505018"
    login_twitter(driver, username, password)

tagPage = inputTag(driver, tag_input)
# tagPage = driver
FingFer(tagPage)
driver2scroll = driver
scrollAndGather(driver2scroll, scrolls)
#Setting up base URL:

# driver = webdriver.Firefox()
# #replace with URL of choice
# driver.base_url = "https://twitter.com/reshadbinharun/following"
# driver.get(driver.base_url)

#Strategy to address infinite scroll
    

# searchBox.send_keys("RETURN")
# scrolls = 10
