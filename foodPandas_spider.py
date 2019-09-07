from foodPandas_url import FoodPandaUrl
from foodPandas_html import FoodPandaHtml

class FoodPandaSpider():
    def __init__(self):
        pass

    def get_url(self):
        self.url_downloader = FoodPandaUrl()
        self.url_downloader.goto_panda()

    def process_html(self):
        self.html_processer = FoodPandaHtml(self.url_downloader.url_result)
        self.html_processer.html_process()

if __name__ == '__main__':
    obj = FoodPandaSpider()
    obj.get_url()
    obj.process_html()
