from bs4 import BeautifulSoup
import traceback
import os
import time
import datetime
import re
import sys
import requests
import csv

class FoodPandaHtml():
    def __init__(self, url_list):
        self.url_list = url_list
        self.result = []

    def get_dish_info(self,url):
        result = []

        r2 = requests.get(url)
        soup2 = BeautifulSoup(r2.text,'lxml')

        extract_date = datetime.datetime.now().strftime("%Y/%m/%d")

        try:
            store_name = soup2.find('h1',{'class':'fn'}).text
        except:
            store_name = '--'
        #price comment given by Foodpandas
        store_price = '$'*len(soup2.find('ul',{'class':'vendor-info-main-details-cuisines'})\
                          .find_all('li')[0].find_all('span'))

        store_type = [x.text for x in soup2.find('ul',{'class':'vendor-info-main-details-cuisines'}).find_all('li')[1:]]
        store_type = '/'.join(store_type)

        #All information about dishes
        dish_info = soup2.find('div',{'class':'menu__items'})

        #Category for the dishes
        category_title = [title.text for title in dish_info.find_all('h2', {'class':'dish-category-title'})]
        dish_list = [title for title in dish_info.find_all('ul', {'class':'dish-list'})]

        #Dish name grouped by category as a list of lists
        dish_name_in_category = []
        for dish in dish_list:
            dish_name_in_category \
            .append([name.text.strip() for name in dish.find_all('h3',{'class':'dish-name fn p-name'})])

        #Raw dish price grouped by category as a list of lists
        dish_price_in_category = []
        for dish in dish_list:
            dish_price_in_category \
            .append([name.text for name in dish.find_all('span',{'class':'price p-price'})])

        #Extract price value from raw dish price
        new_dish_price_in_category = []
        for price_in_cat in dish_price_in_category:
            new_price_in_cat = []
            for raw_price in price_in_cat:
                new_price = re.findall('[0-9]+\.[0-9]+', raw_price)
                new_price_in_cat.extend(new_price)
            new_dish_price_in_category.append(new_price_in_cat)


        for i in range(len(dish_name_in_category)):
            for j in range(len(dish_name_in_category[i])):
                dish_refined = []
                dish_refined.extend((extract_date,
                                     store_name,
                                     store_price,
                                     store_type,
                                     category_title[i],
                                     dish_name_in_category[i][j],
                                     new_dish_price_in_category[i][j]))
                result.append(dish_refined)

        return result


    def get_dish_info_bulk(self,url_list):
        count = 1
        results = []
        title = ['extract_date','store_name','store_price_lv','store_type','dish_type','dish_name','dish_price']
        results.append(title)
        for url in url_list:
            percentage = str(round(count/len(url_list)*100,2))
            sys.stdout.write('\rprocessing url: {}\n{} % complete'.format(url, percentage))

            dishes = self.get_dish_info(url)
            for item in dishes:
                results.append(item)
            count += 1

        return results

    def to_csv(self, dish_list):
        extract_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with open("{}_foodPanda_dish.csv".format(extract_date), "w") as f:
            writer = csv.writer(f)
            writer.writerows(dish_list)

    def html_process(self):
        start = datetime.datetime.now()

        print('extracting start')
        self.results = self.get_dish_info_bulk(self.url_list)
        self.to_csv(self.results)
        total_time = datetime.datetime.now() - start
        print('\nRuntime: {}'.format(total_time))
