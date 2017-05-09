# coding=utf-8
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
# import urllib

sina_account = "jhonsonlai@sina.com"
sina_passwd = ""
douyu_login_url = ("https://api.weibo.com/oauth2/authorize?client_id="
                   "979098171&redirect_uri=http://www.douyu.com"
                   "/member/oauth/signin/weibo")

chrome_path = ("C:/Program Files (x86)/Google/"
               "Chrome/Application/chromedriver.exe")


def get_douyu_list(f_list_html):
    soup = BeautifulSoup(f_list_html, "lxml")
    print """
           ___   ____   __  __ __  __  __  __
          / _ \ / __ \ / / / / \ \/ / / / / /
         / // // /_/ // /_/ /   \  / / /_/ /
        /____/ \____/ \____/    /_/  \____/
        """
    for index, fl in enumerate(soup.find_all('li')):
        ftitle = fl.find("a", target=True)
        ftime = fl.find("a", class_="head-ico4")
        fname = fl.find("a", class_="head-ico2")
        # froom = fl.find("a", class_="head-ico3")
        print ("\n----------- " + str(index) + " "
               + fname.get_text()
               + " ------------")
        if ftime:
            print ftime.get_text(), ftitle.get_text().encode("gb18030")
        else:
            print ftitle.get_text().encode("gb18030")


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
fl_div = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "o-history")))
fl_hover = ActionChains(browser).move_to_element(fl_div)
fl_hover.perform()
fl_div = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "h-list")))
# print fl_div.get_attribute('innerHTML').encode('gb18030')
with open('h-list.html', 'w') as fo:
    fo.write(fl_div.get_attribute('innerHTML').encode('gb18030'))

get_douyu_list(fl_div.get_attribute('innerHTML'))
browser.close()
