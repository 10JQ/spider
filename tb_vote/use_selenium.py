from selenium import webdriver  
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup  
import random   
import re  
import time   
import xlwt  
import os
import subprocess

# 初始化火狐浏览器  
def init(url): 
    # firefox配置
    # 无图
    firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)

    # headless模式
    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.set_headless()

    firefox_login=webdriver.Firefox(firefox_profile=firefox_profile, firefox_options= firefox_options)
    try:
        firefox_login.get(url)
    except WebDriverException:
        firefox_login.quit()
        return -1
    # firefox_login.maximize_window()
    # firefox_login.set_window_size(1024, 400)
    firefox_login.set_window_position(0,0)
    return firefox_login

def search(firefox_login):
    firefox_login.find_element_by_id('q').clear()  
    firefox_login.find_element_by_id('q').send_keys(u'投票')     
    firefox_login.find_element_by_class_name("btn-search").click()   

    firefox_login.find_element_by_link_text(u'销量').click()

    time.sleep(random.randint(5,8)) 

def get_vote_items(firefox_login):
    items = firefox_login.find_elements_by_class_name("item")
    for item in items:
        try:
            price = item.find_element_by_css_selector('div.price.g_price.g_price-highlight')
            price_f = float(price.text[1:])
            if price_f < 10:
                item_name = item.find_element_by_css_selector("div.row.row-2.title")
                item_url = item_name.find_element_by_css_selector("a.J_ClickStat").get_attribute("href")
                id_index = item_url.find('id=')
                item_id = item_url[id_index+3:id_index+15]
                shop_name = item.find_element_by_css_selector("a.shopname.J_MouseEneterLeave.J_ShopInfo")
                deal_count = item.find_element_by_css_selector("div.deal-cnt")
                
                print(item_name.text, end="\t")
                print(shop_name.text, end="\t")
                print(deal_count.text)
                print(item_id)

        except NoSuchElementException:
            pass


if __name__=='__main__':  
    url='https://www.taobao.com'

    firefox_login = init(url)
    search(firefox_login)
    get_vote_items(firefox_login)

    time.sleep(5)
    firefox_login.quit()