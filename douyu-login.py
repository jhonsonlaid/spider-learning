# coding=utf-8
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import bs4
import time
# import urllib

sina_account = "jhonsonlai@sina.com"
sina_passwd = ""
douyu_login_url = ("https://api.weibo.com/oauth2/authorize?client_id="
                   "979098171&redirect_uri=http://www.douyu.com"
                   "/member/oauth/signin/weibo")

chrome_path = ("C:/Program Files (x86)/Google/"
               "Chrome/Application/chromedriver.exe")


# def get_page(url):
#     page = urllib.urlopen(url)
#     content = page.read()
#     return content


# page_content = get_page(douyu_login_url)
# print page_content.decode("utf-8")

browser = webdriver.Chrome(chrome_path)
# browser.implicitly_wait(10)
browser.get(douyu_login_url)
browser.maximize_window()
account_elem = browser.find_element_by_id('userId')
account_elem.send_keys(sina_account)
passwd_elem = browser.find_element_by_id('passwd')
passwd_elem.send_keys(sina_passwd)
time.sleep(0.5)
submit_elem = browser.find_element_by_class_name("WB_btn_login")
submit_elem.click()

# perform hover
fl_div = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((
        By.CLASS_NAME, "o-history")))
fl_hover = ActionChains(browser).move_to_element(fl_div)
fl_hover.perform()
fl_div = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((
        By.CLASS_NAME, "h-list")))
print fl_div.get_attribute('innerHTML').encode('gb18030')
with open('h-list.html', 'w') as fo:
    fo.write(fl_div.get_attribute('innerHTML').encode('gb18030'))
browser.close()
