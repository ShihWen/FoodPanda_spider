import re
import sys
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class FoodPandaHtmlDownloader():
    def __init__(self):
        self.result = []

    def get_html(self, url_list):
        start = datetime.datetime.now()
        count = 1
        percentage = str(round(count/len(url_list)*100,2))
        for url in url_list:
            percentage = str(round(count/len(url_list)*100,2))
            sys.stdout.write('\rdownloading {} url, progress {} '.format(count, percentage))
            r = requests.get(url)
            self.result.append(r.text)
            count += 1
        total_time = datetime.datetime.now() - start
        print('\nRuntime: {}'.format(total_time))

    def get_html_single(self, url):
        r = requests.get(url)
        self.result.append(r.text)

    #Reference from:
    #https://pythontips.com/2019/05/29/speeding-up-python-code-using-multithreading/
    def get_html_multi(self, url_list):
        print('dowloading {} Html contents...'.format(len(url_list)))
        start = datetime.datetime.now()
        processes = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for url in url_list:
                processes.append(executor.submit(self.get_html_single, url))

        total_time = datetime.datetime.now() - start
        print('\nRuntime for html download: {}'.format(total_time))
