'''
By: Jonah Stegman
feature extraction for ENGG*6500 project
This file looks up the page rank of a url.
'''

import pandas as pd
from selenium import webdriver
import glob
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

# read in dataset and format it for lookup
df = pd.read_csv("data/malicious_phish.csv")
df['URL2'] = df['URL']
df["URL2"] = df["URL2"].str.replace('http://','')
df["URL2"] = df["URL2"].str.replace('https://','')
df["URL2"] = df["URL2"].str.replace('ftp://','')
df["URL2"] = df["URL2"].str.split("/").str[0]
df = df[555100:]
df = df.reset_index(drop=True)
url = "https://www.domcop.com/openpagerank/"
#configure seleniums firefox profiles
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxprofile = webdriver.FirefoxProfile()
fireFoxprofile.set_preference("browser.download.folderList", 2)
fireFoxprofile.set_preference("browser.download.manager.showWhenStarting", False)
fireFoxprofile.set_preference("browser.download.dir", os.path.dirname(__file__))
fireFoxprofile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
fireFoxprofile.set_preference("browser.helperApps.neverAsk.openFile","text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
fireFoxprofile.set_preference("browser.helperApps.alwaysAsk.force", False)
fireFoxprofile.set_preference("browser.download.manager.useWindow", False)
fireFoxprofile.set_preference("browser.download.manager.focusWhenStarting", False)
fireFoxprofile.set_preference("browser.helperApps.neverAsk.openFile", "")
fireFoxprofile.set_preference("browser.download.manager.alertOnEXEOpen", False)
fireFoxprofile.set_preference("browser.download.manager.showAlertOnComplete", False)
fireFoxprofile.set_preference("browser.download.manager.closeWhenDone", True)
#fireFoxOptions.set_headless()

#open webpage for webscraping of page ranks
browser = webdriver.Firefox(firefox_profile=fireFoxprofile,firefox_options=fireFoxOptions)
browser.get(url)
num = 0
rank = []

while num < df['URL2'].count() + 1:
    total = num+1000
    if total > df['URL'].count() + 1:
        total = df['URL'].count() + 1
    df2 = df[num:total]
    num = total
    print(total)
    print(f"rank : {len(rank)}")
    #insert list of URLs for analysis of page rank
    elem = browser.find_element_by_id("domains")
    elem.clear()
    elem.send_keys("\n".join(df2['URL2'].tolist()))
    elem = browser.find_element_by_id("get_page_rank")
    elem.click()
    time.sleep(5)
    # download csv which contains page ranks
    try:
        elem = browser.find_element_by_xpath("//span[contains(text(), 'CSV')]")
        elem.click()
    except Exception:
        time.sleep(8)
        elem = browser.find_element_by_xpath("//span[contains(text(), 'CSV')]")
        elem.click()
    time.sleep(2)
    #get latest downloaded file
    list_of_files = glob.glob('C:\\Users\\Jonah\\Downloads\\*')
    file = max(list_of_files, key=os.path.getctime)
    df3 = pd.read_csv(file)
    #set unknown page ranks to 0
    try:
        df3.loc[df3['Page Rank Value'].str.contains('-', na=True), 'Page Rank Value'] = '0.0'
    except AttributeError:
        pass
    rank += df3['Page Rank Value'].tolist()
    try:
        # gets unknown URLs and sets page ranks to 0
        elem = browser.find_element_by_xpath("//a[@data-domains]")
        elem = elem.get_attribute("data-domains")
        elem = elem.replace("[",'').replace("]",'').replace('"','').split(",")
        for i in elem:
            try:
                i = i.split('?')[0]
                y = df2.loc[df['URL2'].str.contains(i)].index[0]
            except Exception:
                y = df2[(df2 == i).any(axis=1)].index[0]
            rank.insert(y, '0.0')
    except Exception as e:
        pass
    if(len(rank)!=total ):

        print("????")
    #clean up downloaded files
    os.remove(file)
    browser.refresh()
    time.sleep(2)

df['rank'] = rank
df.to_csv("out4.csv", mode='a', index=False, header=False)
