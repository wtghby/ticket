# -*- coding: UTF-8 -*-
# from search import Search
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


# 默认访问一下搜索界面，这样数据接口才能正常访问
class Chrome(object):
    def run(self):
        delay = 3
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # chrome_options.add_argument(('--proxy-server=http://' + '132.58.168.12'))
        driver = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver.exe")

        driver.get("https://www.12306.cn/index/")
        
        time.sleep(delay)
        start = driver.find_element_by_id('fromStationText')
        start.clear()
        start.send_keys('重庆')
        start.send_keys(Keys.ENTER)
        start.send_keys(Keys.TAB)

        end = driver.find_element_by_id('toStationText')
        end.clear()
        end.send_keys('成都')
        end.send_keys(Keys.ENTER)

        query = driver.find_element_by_id('search_one')
        query.click()

        time.sleep(delay)
