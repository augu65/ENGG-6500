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
df = pd.read_csv("out2.csv")
df['URL2'] = df['URL']
df["URL2"] = df["URL2"].str.replace('http://','')
df["URL2"] = df["URL2"].str.replace('https://','')
df["URL2"] = df["URL2"].str.replace('ftp://','')
df["URL2"] = df["URL2"].str.split("/").str[0]

num = 0
url = "https://www.domcop.com/openpagerank/"
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
fireFoxOptions.set_headless()
browser = webdriver.Firefox(firefox_profile=fireFoxprofile,firefox_options=fireFoxOptions)
browser.get(url)
rank = []
while num < df['URL2'].count() + 1:
    total = num+998
    if total > df['URL'].count() + 1:
        total = df['URL'].count() + 1
    df2 = df[num:total]
    num = total + 1
    print(total)
    elem = browser.find_element_by_id("domains")
    elem.clear()
    elem.send_keys("\n".join(df2['URL2'].tolist()))
    elem = browser.find_element_by_id("get_page_rank")
    elem.click()
    time.sleep(5)
    elem = browser.find_element_by_xpath("//span[contains(text(), 'CSV')]")
    elem.click()
    time.sleep(2)
    list_of_files = glob.glob('C:\\Users\\Jonah\\Downloads\\*')  # * means all if need specific format then *.csv
    file = max(list_of_files, key=os.path.getctime)
    df3 = pd.read_csv(file)
    df3.loc[df3['Page Rank Value'].str.contains('-'), 'Page Rank Value'] = '0.0'
    rank += df3['Page Rank Value'].tolist()
    try:
        elem = browser.find_element_by_xpath("//a[@data-domains]")
        elem = elem.get_attribute("data-domains")
        elem = elem.replace("[",'').replace("]",'').replace('"','').split(",")
        for i in elem:
            i = df2.loc[df2['URL2'].str.contains(i)].index[0]
            rank.insert(i, '0.0')
    except Exception as e:
        print(e)

    os.remove(file)
    browser.refresh()
    time.sleep(2)
df['rank'] = rank
df.to_csv("out3.csv",index=False)
