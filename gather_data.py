#reference: https://dev.to/swyx/scraping-my-twitter-social-graph-with-python-and-selenium--hn8
#%matplotlib inline NORE: for Jupyter

#TRY TO AVOID UNABLE TO LOCATE ELEMENT ERRORS
# https://stackoverflow.com/questions/27112731/selenium-common-exceptions-nosuchelementexception-message-unable-to-locate-ele

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

'''
# 20 <li/>'s' in the ordered list of twitter feed are produced by loading a following
#xpath to p containinig tweet: /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[1]/div[1]/div[2]/div[2]/p
#orig tweeter: /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[1]/div[1]/div[2]/div[1]/a/span[1]/strong
#tags in tweet: /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[1]/div[1]/div[2]/div[2]/p/a[1]/b
#xpath to header of tweet containing "context description": /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[1]/div[1]/div[1]/div/span[2]

#comparing tweets:
next to first one:
p -->
/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[...1...]/div[1]/div[2]/div[2]/p
/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[...2...]/div[1]/div[2]/div[2]/p
orig_tweeter -->
/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[...1...]/div[1]/div[2]/div[1]/a/span[1]/strong
/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li[...2...]/div[1]/div[2]/div[1]/a/span[1]/strong

PROTOTYPE to avoid unlocated elements:
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "xpath"))
    )
finally:

'''



def getDataF(driver):
    print("extracting data from each F object")
    allDataF = []
    tweets = []
    orig_tweeter = []
    for i in range(1,5): # only 5 of the first tweets are being parsed
        # try:
        #     Select(tweets.append(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]/div[1]/div[2]/div[2]/p")))
        # # except NoSuchElementException:
        # #     pass
        # # try:    
        #     #Select(orig_tweeter.append(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]/div[1]/div[2]/div[1]/a/span[1]/strong")))
        # except NoSuchElementException:
        #     pass
        #wait at end of every loop for 0.5 s to allow for loading of later list items
        driver.implicitly_wait(2)
        print("extracting {} -th tweet".format(i))
        #tweets.append(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]/div[1]/div[2]/div[2]/p"))
        try:
            pre_tweets_f = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]")))
            tweets_f = pre_tweets_f.find_elements_by_tag_name("p")
            tweets.append(tweets_f[0].text)
        except:
            pass

        #WITHOUT TRY BLOCK:
        # tweets_f = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]").find_elements_by_tag_name("p")
        # print(tweets_f[0].text)
        # tweets.append(tweets_f[0].text)
        
        # orig_tweeter.append(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]/div[1]/div[2]/div[1]/a/span[1]/strong"))
        orig_tweeter.append(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/ol[1]/li["+str(i)+"]").find_elements_by_tag_name("strong")[0].text)
    allDataF.append(tweets)
    # allDataF.append(orig_tweeter)
    return allDataF    




def scrollAndGather(driver, scrolls):
    print("on following/follower page, ready to browse each")
    for i in range(1,scrolls):
        print("on {}-th scroll".format(i))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrollTO takes x-coord and y-coord as inputs
        driver.implicitly_wait(2) # wait for page to load on scroll; may be replace with driver.implicitly_wait()?
        #if window is on full-screen on Firefox, 6 people are loaded each time
        for j in range (1,6):
            print("getting {} -th F on scroll".format(j))
            driver.implicitly_wait(2)
            try:
                link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div["+str(i)+"]/div["+str(j)+"]/div/div/div/div[2]/div/div/a")))
                driver.get(link.get_attribute('href')) #get link for each Following
                #function to scrape data from new person
                driver.implicitly_wait(1)
                print(getDataF(driver))
                driver.back()
                driver.implicitly_wait(2)
            except:
                pass
            #WITHOUT try blocks
            # link = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div["+str(i)+"]/div["+str(j)+"]/div/div/div/div[2]/div/div/a")
            # driver.get(link.get_attribute('href')) #get link for each Following
            # #function to scrape data from new person
            # driver.implicitly_wait(1)
            # print(getDataF(driver))
            # driver.back()
            # driver.implicitly_wait(2)
        #gather
        '''
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[27]/div[1]/div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[27]/div...[2].../div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[27]/div...[3].../div/div/div/div[2]/div/div/a
        /html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div[27]/div...[4].../div/div/div/div[2]/div/div/a
        The isolated div indexes change on every scroll
        '''
        print(i)

def inputTag(driver, tag):
    searchBox = driver
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"search-query\"]")))
        element.send_keys(tag)
    except:
        print("could not locate search-box")
        pass

    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"global-nav-search\"]/span/button")))
        element.click()
    except:
        print("could not click")
        pass

    # searchBox.find_element_by_xpath("//*[@id=\"search-query\"]").send_keys(tag)
    # searchBox.find_element_by_xpath("//*[@id=\"global-nav-search\"]/span/button").click()
    # searchBox.implicitly_wait(2) # wait for load
    print("sent out search criteria")
    return searchBox

#FireFox's xpath seem to be indexed slightly differently from Chrome's
def FingFer(driver):
    #print("Please switch to full-screen to accommodate scraping with infinite scroll.")
    print("On Company page, and ready to browse followers/following")
    while True:
        choice = int(input("Get data on following (1) or followers (2)? Enter integer input please. "))
        if choice == 1:
            try:
                following = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a")))
                link = following.get_attribute("href")
                try:
                    countTag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a/span[2]")))
                    count = int(countTag.get_attribute("data-count"))
                    print("This tag has {} following.".format(count))
                    driver.get(link)
                    break
                except:
                    pass    
            except:
                print("could not locate search-box")
                pass
            #WITHOUT TRY BLOCK
            # following = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a")
            # link = following.get_attribute("href")
            # count = int(driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/div[2]/ol[1]/li[1]/div[2]/div/div/div/div/div[1]/ul/li[2]/a/span[2]").get_attribute("data-count"))
            # print("This tag has {} following.".format(count))
            # driver.get(link)
            # break
        elif choice == 2:
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
    username = input("user name : ")
    password = getpass("password  : ")
    login_twitter(driver, username, password)
driver.implicitly_wait(2)
tagPage = inputTag(driver, tag_input)
# tagPage = driver
FingFer(tagPage)
driver2scroll = driver
driver.implicitly_wait(2)
scrollAndGather(driver2scroll, scrolls)
#Setting up base URL:

# driver = webdriver.Firefox()
# #replace with URL of choice
# driver.base_url = "https://twitter.com/reshadbinharun/following"
# driver.get(driver.base_url)

#Strategy to address infinite scroll
    

# searchBox.send_keys("RETURN")
# scrolls = 10
