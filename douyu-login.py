# coding=utf-8
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import time


def get_page(url):
    page = urllib.urlopen(url)
    content = page.read()
    return content


douyu_login_url = "https://api.weibo.com/oauth2/authorize?client_id=979098171&\
redirect_uri=http://www.douyu.com/member/oauth/signin/weibo"

chrome_path = "C:/Program Files (x86)/Google/\
Chrome/Application/chromedriver.exe"

# page_content = get_page(douyu_login_url)
# print page_content.decode("utf-8")

browser = webdriver.Chrome(chrome_path)
browser.get(douyu_login_url)
account_elem = browser.find_element_by_id('userId')
account_elem.send_keys('user@sina.com')
passwd_elem = browser.find_element_by_id('passwd')
passwd_elem.send_keys('pwd')
time.sleep(0.2)
submit_elem = browser.find_element_by_class_name("WB_btn_login")
submit_elem.click()
