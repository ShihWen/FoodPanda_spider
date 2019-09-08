import re
import sys
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class FoodPandaHtmlDownloader():
    def __init__(self):
        self.result = []

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
