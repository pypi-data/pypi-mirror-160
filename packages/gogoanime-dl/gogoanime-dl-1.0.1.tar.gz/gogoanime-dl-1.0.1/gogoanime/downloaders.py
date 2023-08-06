"""
@author: AuraMoon55
@contact: garganshul553@gmail.com
@license: MIT License, see LICENSE file
Copyright (C) 2022
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests, time, zipfile, io, os



def get_chromedriver():
  cmd = "apt-get update&&apt install chromium-chromedriver&&cp /usr/lib/chromium-browser/chromedriver /usr/bin"
  os.system(cmd)
  return 'chromedriver'



def dlfiles(File, url):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  browser = webdriver.Chrome(get_chromedriver() ,options=chrome_options)
  try:
   # t1 = time.time()
    timeout = 100
    browser.get(url)
    element = browser.find_element(By.ID, "download")
    element.click()
    what_is_this = WebDriverWait(browser, timeout).until(
      EC.presence_of_element_located(
        (By.CLASS_NAME, "clickdownload")
      )
    )
    for x in browser.find_elements(By.CLASS_NAME, "clickdownload"):
      option = input(f"Do You Want To Download This Anime in {x.get_property('text')}p Quality?\nType y/n")
      if option.lower()[0] == "y":
        b = requests.get(x.get_property("href"))
        open(f'{File}-{x.get_property("text")}p.mp4',"wb").write(b.content)
       # print(f"Time Taken To Download: {get_readable_time(time.time()-t2)}")
        return browser.quit()
      else:
      #  t2 = time.time()
        pass
    browser.quit()
    
  except TimeoutException as x:
    browser.quit()
    return print(x)
