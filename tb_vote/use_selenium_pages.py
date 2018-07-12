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
import os
import schedule

# 初始化火狐浏览器  
def init(url): 
    # firefox配置
    # 无图
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('permissions.default.image', 2)

    # headless模式
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_headless()

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


#数据库连接函数      
def connDB():  
    # 打开数据库连接
    db = pymysql.connect("114.215.99.71","root","yan33ppJun9966A","tb_vote")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    return (db, cursor)

#写入数据库
def insertDB(db, cursor, item_data):
    sql = """INSERT INTO vote_price1(item_id, item_name, shop_name, deal_count, price, scan_time) VALUES('{0}', '{1}', '{2}', '{3}', {4}, now())""".format(item_data[0], item_data[1], item_data[2], item_data[3], item_data[4])
    cursor.execute(sql)
    db.commit()
  
#关闭数据库连接  
def exitConn(db, cursor):
    db.close() 

def get_vote_items_010(firefox_login):
    db, cursor = connDB()
    items = firefox_login.find_elements_by_class_name("item")
    n = 0
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

            if price_f > 0.1 and price_f <= 1:
                insertDB(db, cursor, (item_id, item_name.text, shop_name.text, deal_count.text, price_f))
                n += 1
        except NoSuchElementException:
            pass

    exitConn(db, cursor)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Numbers:', n)

    return n

def get_vote_items_pages(firefox_login, url):
    n = 0
    while True:
        time.sleep(5)
        # 获取数据
        n += get_vote_items_010(firefox_login)
        # 获取其他页面链接
        other_page_links = firefox_login.find_elements_by_css_selector("a.J_Ajax.num.icon-tag")
        find_nextpage = False
        for other_page_link in other_page_links:
            trace = other_page_link.get_attribute('trace')
            # 找到下一页链接，跳转
            if trace == 'srp_bottom_pagedown':
                url = other_page_link.get_attribute('href')
                find_nextpage = True
                other_page_link.click()

                # 跳转后等待
                locator = (By.LINK_TEXT, '下一页')
                try:
                    WebDriverWait(firefox_login, 10, 0.5).until(EC.presence_of_element_located(locator))
                except TimeoutException:
                    # 打开页面失败后刷新
                    print('refresh')
                    firefox_login.refresh()
                break
        # 没有下一页链接，退出
        if not find_nextpage:
            break
        
    return n

def job():
    url_price_1 = 'https://s.taobao.com/search?q=%E6%8A%95%E7%A5%A8%E7%AE%B1&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180712&ie=utf8&sort=default&bcoffset=4&p4ppushleft=2%2C48&ntoffset=4&filter=reserve_price%5B0.11%2C1%5D&s=0'

    firefox_cmd = 'taskkill /F /IM firefox.exe'
    firefox_gd = 'taskkill /F /IM geckodriver.exe'
    os.system(firefox_cmd)
    os.system(firefox_gd)

    firefox_login = init(url_price_1)
    firefox_login.refresh()
    firefox_login.refresh()
    n = get_vote_items_pages(firefox_login, url_price_1)
    print('Total number:', n)

    time.sleep(5)
    firefox_login.quit()
    time.sleep(5)
        
    os.system(firefox_cmd)
    os.system(firefox_gd)

        

if __name__=='__main__': 
    job()
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
