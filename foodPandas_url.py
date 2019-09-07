from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.expected_conditions as EC

from bs4 import BeautifulSoup
import time
import datetime

class FoodPandaUrl():
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(chrome_options = option)
        self.url_result = None

    def timePractice(self):
        time.sleep(5)

    def page_scrolling(self):
        while True:
            count = 1
            no_update = 0
            pics = self.driver.find_elements_by_class_name('vendor-picture')
            last_pic = pics[-1]
            self.driver.execute_script("arguments[0].scrollIntoView();", last_pic)
            print('scroll {}'.format(count))
            count += 1

            #Check if the site page is updated with new data by number of store pictures
            #If site page stop updating, check how many times the page has loading new data,
            # if less than 8*, refresh the page. *depends on the your preferance.
            while len(pics) == len(self.driver.find_elements_by_class_name('vendor-picture')):
                time.sleep(0.25)
                if len(pics) < len(self.driver.find_elements_by_class_name('vendor-picture')):
                    pics = self.driver.find_elements_by_class_name('vendor-picture')
                    last_pic = pics[-1]
                    print('scroll {}'.format(count))
                    count += 1
                    self.driver.execute_script("arguments[0].scrollIntoView();", last_pic)
                    no_update = 0
                else:
                    no_update += 1
                    if no_update % 2 == 0:
                        print('waiting for updates...')
                if no_update > 20:
                    break
            if count > 8:
                break
            else:
                self.driver.refresh()
                print('refresh page')
        total_stores = len(self.driver.find_elements_by_class_name('vendor-picture'))

        return total_stores

    def url_list(self,soup):
        section = ['opened', 'closed']
        count = 0
        url_root = 'https://www.foodpanda.com.tw'
        res_name_location = []
        url_res_list = []

        for item in section:
            class_key = 'vendor-list ' + item
            res_list = soup.find('ul',{'class':class_key}).find_all('li',{'class':'','id':''})

            for i in range(len(res_list)):

                if res_list[i].find('a') is not None:
                    url_res = url_root + res_list[i].find('a')['href']
                    url_res_list.append(url_res)

        return url_res_list

    def teardown(self):
        self.driver.close()

    def goto_panda(self):
        start = datetime.datetime.now()
        #Copy the url after entering your address at https://www.foodpanda.com.tw/
        url = 'https://www.foodpanda.com.tw/restaurants/lat/' \
                '25.03754169999999/lng/121.5644327/city/%E4%BF%A1%E7%BE%A9%E5%8D%80/' \
                'address/%25E8%2587%25BA%25E5%258C%2597%25E5%25B8%2582%25E6%2594%25BF%2' \
                '5E5%25BA%259C%252C%252011008%25E5%258F%25B0%25E7%2581%25A3%25E5%258F%25B' \
                '0%25E5%258C%2597%25E5%25B8%2582%25E4%25BF%25A1%25E7%25BE%25A9%25E5%258D%' \
                '2580%25E5%25B8%2582%25E5%25BA%259C%25E8%25B7%25AF1%25E8%2599%259F/%25E5%' \
                '25B8%2582%25E5%25BA%259C%25E8%25B7%25AF/1%25E8%2599%259F%2520%25E8%2587%' \
                '25BA%25E5%258C%2597%25E5%25B8%2582%25E6%2594%25BF%25E5%25BA%259C?postcode=11008'
        self.driver.get(url)
        ui.WebDriverWait(self.driver,10).until(EC.presence_of_element_located( \
            (By.CSS_SELECTOR,
            'body > div.page-wrapper > div > main > div > div.restaurants__list >' \
                'section.vendor-list-section.opened > ul > li:nth-child(1) > a > figure' \
                '> figcaption > span > span')))
        print('waiting DONE')

        total_stores = self.page_scrolling()
        html = self.driver.page_source
        soup = BeautifulSoup(html,'lxml')
        self.url_result = self.url_list(soup)
        self.teardown
        print(total_stores, len(self.url_result), '\n')
