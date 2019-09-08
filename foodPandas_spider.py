from foodPandas_url import FoodPandaUrl
from foodPandas_html_download import FoodPandaHtmlDownloader
from foodPandas_html_process import FoodPandaHtmlProcesser

class FoodPandaSpider():
    def __init__(self):
        self.url_downloader = FoodPandaUrl()
        self.html_downloader = FoodPandaHtmlDownloader()
        self.html_processer = FoodPandaHtmlProcesser()

    def run(self):
        self.url_downloader.goto_panda()
        self.html_downloader.get_html_multi(self.url_downloader.result)
        self.html_processer.html_process(self.html_downloader.result)

if __name__ == '__main__':
    obj = FoodPandaSpider()
    obj.run()
