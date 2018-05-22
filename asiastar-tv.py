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

g_adsl_account = {"name": "adslgo",
				"username": "h5sva026",
				"password": "123456"}


class Adsl(object):
    #==============================================================================
    # __init__ : name: adsl名称
    #==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

		
    #==============================================================================
    # set_adsl : 修改adsl设置
    #==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

	
    #==============================================================================
    # connect : 宽带拨号
    #==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        subprocess.run(cmd_str, shell=True)
        #os.system(cmd_str)
        time.sleep(1)

		
    #==============================================================================
    # disconnect : 断开宽带连接
    #==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        subprocess.run(cmd_str, shell=True)
        #os.system(cmd_str)
        time.sleep(1)

	
    #==============================================================================
    # reconnect : 重新进行拨号
    #==============================================================================
    def reconnect(self):
        self.disconnect()
        self.connect()


# 初始化火狐浏览器  
def init(url): 
    # firefox配置
    # 无图
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    #firefox_profile.set_preference('browser.migration.version', 9001)#部分需要加上这个
    # 禁用css
    #firefox_profile.set_preference('permissions.default.stylesheet', 2)
    # 禁用flash
    #firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # 禁用js
    #firefox_profile.set_preference('javascript.enabled', 'false')

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
    firefox_login.set_window_size(1024, 400)
    firefox_login.set_window_position(0,0)
    return firefox_login  

# 刷新页面
def refresh_current_page(firefox_login):
    try:
        firefox_login.refresh()
    except WebDriverException:
        return -1

# 判断alert是否弹出，捕获异常
def is_alert_present(firefox_login):
    try: 
        firefox_login.switch_to_alert()
    except NoAlertPresentException: 
        return False
    return True

# 一定时间内等待alert弹出
def wait_alert_present(firefox_login, timeout = 10):
    for i in range(0, timeout):
        if is_alert_present(firefox_login) == True:
            return True
        else:
            time.sleep(1)
        return False

# 取得alert文本
def get_alert_text(firefox_login):
    alert = firefox_login.switch_to_alert()
    return alert.text





if __name__=='__main__':  
    votes_previous = 0
    votes_current = 0
    votes_fault_times = 0
    
    adsl = Adsl()

    # 帅锅
    # url='http://www.asiastar-tv.com/usa/vote/Vote_Show.asp?InfoId=57a53a51&ClassId=33&Topid=0'
    # Otani Noodle
    # url='http://www.asiastar-tv.com/usa/vote/Vote_Show.asp?InfoId=56a53a51&ClassId=33&Topid=0'
    # 粤煌
    # url='http://www.asiastar-tv.com/usa/vote/Vote_Show.asp?InfoId=49a56a51&ClassId=33&Topid=0'
    # 福碗
    url='http://www.asiastar-tv.com/usa/vote/Vote_Show.asp?InfoId=51a48a51&ClassId=33&Topid=0'
    # 玉盛园
    # url='http://www.asiastar-tv.com/usa/vote/Vote_Show.asp?InfoId=50a55a51&ClassId=33&Topid=0'

    firefox_login=init(url)
    if firefox_login == -1:
        print("not online, reconnect...")
        adsl.reconnect()
        firefox_login=init(url)

    for i in range(0, 10000):
        # 刷新
        if refresh_current_page(firefox_login) == -1:
            print("not online, reconnect...")
            adsl.reconnect()
            continue
            

        print("{} vote number".format(time.ctime()), i+1, end=":\t")

        # 取得投票前的票数
        locator = (By.CLASS_NAME, 'info')
        try:
            WebDriverWait(firefox_login, 10, 0.5).until(EC.presence_of_element_located(locator))
            time.sleep(2)
            votes_previous = int(firefox_login.find_element_by_xpath('//font[@color="red"]').text)
        except TimeoutException:
            votes_fault_times += 0
        except UnexpectedAlertPresentException:
            votes_fault_times += 0
        except NoSuchElementException:
            pass
        
        print("votes_previous:", votes_previous, end="\t")

        # 投票
        firefox_login.find_element_by_class_name("thickbox").click()
        
        if wait_alert_present(firefox_login) == True:
            alert = firefox_login.switch_to_alert()
            alert.accept()

        if wait_alert_present(firefox_login) == True:
            alert = firefox_login.switch_to_alert()
            alert.accept()
        
        # 取得投票后的票数
        try:
            WebDriverWait(firefox_login, 10, 0.5).until(EC.presence_of_element_located(locator))
            time.sleep(2)
            votes_current = int(firefox_login.find_element_by_xpath('//font[@color="red"]').text)
        except TimeoutException:
            votes_fault_times += 0
        except UnexpectedAlertPresentException:
            votes_fault_times += 0
        except NoSuchElementException:
            pass

        print("votes_current:", votes_current)

        # TODO

        # 票数不动，累计3次，暂停十分钟
        if votes_current == votes_previous:
            votes_fault_times += 1
            if votes_fault_times >=3:
                print("{}: votes fault times >=3, sleep 10 minutes".format(time.ctime()))
                votes_fault_times = 0
                time.sleep(600)
        else:
            votes_fault_times = 0
        
        # 达到指定票数后结束程序
        
        # 重新连接ADSL
        adsl.reconnect()

    firefox_login.quit()
