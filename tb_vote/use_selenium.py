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
import pymysql
import datetime

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

#数据库连接函数      
def connDB():  
    # 打开数据库连接
    db = pymysql.connect("114.215.99.71","root","yan33ppJun9966A","tb_vote")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    return (db, cursor)

#写入数据库
def insertDB(db, cursor, item_data):
    sql = """INSERT INTO vote(item_id, item_name, shop_name, deal_count, price, scan_time) VALUES('{0}', '{1}', '{2}', '{3}', {4}, unix_timestamp(now()))""".format(item_data[0], item_data[1], item_data[2], item_data[3], item_data[4])
    cursor.execute(sql)
    db.commit()
  
#关闭数据库连接  
def exitConn(db, cursor):
    db.close() 

def get_vote_items(firefox_login):
    db, cursor = connDB()
    items = firefox_login.find_elements_by_class_name("item")
    other_keyword = '助力'
    for item in items:
        try:
            price = item.find_element_by_css_selector('div.price.g_price.g_price-highlight')
            price_f = float(price.text[1:])
            item_name = item.find_element_by_css_selector("div.row.row-2.title")
            if price_f < 10 or other_keyword in item_name.text:
                item_url = item_name.find_element_by_css_selector("a.J_ClickStat").get_attribute("href")
                id_index = item_url.find('id=')
                item_id = item_url[id_index+3:id_index+15]
                shop_name = item.find_element_by_css_selector("a.shopname.J_MouseEneterLeave.J_ShopInfo")
                deal_count = item.find_element_by_css_selector("div.deal-cnt")
                
                print(item_name.text, end="\t")
                print(shop_name.text, end="\t")
                print(deal_count.text)
                print(price_f)
                print(item_id)

                insertDB(db, cursor, (item_id, item_name.text, shop_name.text, deal_count.text, price_f))

        except NoSuchElementException:
            pass

    exitConn(db, cursor)

def get_vote_items_010(firefox_login):
    db, cursor = connDB()
    items = firefox_login.find_elements_by_class_name("item")
    for item in items:
        try:
            price = item.find_element_by_css_selector('div.price.g_price.g_price-highlight')
            price_f = float(price.text[1:])
            item_name = item.find_element_by_css_selector("div.row.row-2.title")
            item_url = item_name.find_element_by_css_selector("a.J_ClickStat").get_attribute("href")
            id_index = item_url.find('id=')
            item_id = item_url[id_index+3:id_index+15]
            shop_name = item.find_element_by_css_selector("a.shopname.J_MouseEneterLeave.J_ShopInfo")
            deal_count = item.find_element_by_css_selector("div.deal-cnt")

            insertDB(db, cursor, (item_id, item_name.text, shop_name.text, deal_count.text, price_f))

        except NoSuchElementException:
            pass

    exitConn(db, cursor)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__=='__main__':  
    url='https://www.taobao.com'
    url_010 = 'https://s.taobao.com/search?q=%E6%8A%95%E7%A5%A8&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&filter=reserve_price%5B0.1%2C0.1%5D'

    while True:
        # firefox_login = init(url)
        # search(firefox_login)
        # get_vote_items(firefox_login)
        firefox_login = init(url_010)
        get_vote_items_010(firefox_login)

        time.sleep(5)
        firefox_login.quit()

        time.sleep(1800)