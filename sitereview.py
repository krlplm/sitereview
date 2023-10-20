##################################################################################################################################
# Script to fetch the Domain and IP data from Risk IQ, VirusTotal API and to scrape the categorization from Symantec site review using selenium.
# Author : Cyberdude
##################################################################################################################################

#from argparse import ArgumentParser
#from bs4 import BeautifulSoup
import json
import requests
import config
import os
import re
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.by import By #latest changes
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
import csv


class siteReview():
    def __init__(self):
        #To instantiate the chrome browser
        s = Service(config.CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=s)
        #To instantiate the chrome browser in macos
        #self.driver = webdriver.Chrome()

    def ioc_search(self, entity):
        url = 'https://sitereview.bluecoat.com/#/'
        self.driver.get(url)
        self.driver.find_element(By.ID, 'txtUrl').send_keys(entity)
        self.driver.find_element(By.ID, 'btnLookup').click()
        #With out this sleep function, the site review rejects the requests. This will help to throttle the requests.
        sleep(6)

        try:
            #Parsing the sitereview response page for the element of interest
            cat = self.driver.find_element(By.XPATH, '//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[1]/span')
            if self.driver.find_element(By.XPATH, '//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[2]/span'):
                cat2 = self.driver.find_element(By.XPATH, '//*[@id="submissionForm"]/span/span[1]/div/div[2]/span[2]/span')
                if "Last Time" in cat2.text:
                    category = cat.text
                else:
                    category = cat.text + "|" + cat2.text
            else:
                category = cat.text
        except:
            category = 'error'
        return category

#Function to process list of domains/IP Addresses
def lst_parse(lst):
    bot = siteReview()
    with open(os.path.join(lst), 'r') as f, \
         open("results.csv", "w", newline="") as csvfile:

        fieldnames = ["Domain/IP", "Category"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for ent in f:
            entity = ent.strip()
            #print('Processing:', entity)

            val = bot.ioc_search(entity)

            #Print to the console
            print(entity, val, sep=",")

            # Write each row to the CSV file
            writer.writerow({"Domain/IP": entity, "Category": val})

#Function to process single domain/IP Address
def cmd_parse(cmd):
    entity = cmd
    bot = siteReview()
    val = bot.ioc_search(entity)
    print(entity, val, sep=",")

def main():
    p = ArgumentParser()
    p.add_argument("-l", "--lst", type=str, help="Submit domain/IP list separated by new line specifying the absolute path of file")
    p.add_argument("-c", "--cmd", type=str, help="Enter the single domain/IP")
    args = p.parse_args()
    if args.lst:
        print('ioc,Symantec_Sitereview')
        lst_parse(args.lst)
    elif args.cmd:
        print('ioc,Symantec_Sitereview')
        cmd_parse(args.cmd)
    else:
        print("\n" + "Note: Please supplement the single domain/IP by using switch -c or a list of domains/IPs with the path by using switch -l" + "\n")


if __name__ == "__main__":
    main()
else:
    pass